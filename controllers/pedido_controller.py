"""Rotas e operacoes de interface para pedidos."""

import math
from itertools import zip_longest
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, redirect, render_template, request, url_for, flash, session

from database.db import db
from controllers.auth_required import login_required
from models.cliente import Cliente
from models.material import Material
from models.pedido import Pedido
from models.consumo_material import ConsumoMaterial
from services.consumo_material_service import consumos_do_pedido, planejar_consumos
from services.estoque_service import consumir_material, devolver_material, registrar_movimentacao
from services.constantes import STATUS_PEDIDO
from services.pedido_service import (
    atualizar_status_com_notificacao,
    calcular_melhor_aproveitamento,
    converter_para_metros,
    formatar_area,
    formatar_metros,
    normalizar_busca,
)

pedido_bp = Blueprint("pedido", __name__)

ORDEM_CATEGORIAS = {
    "Adesivo": 1,
    "Lona": 2,
    "Tecido": 3,
}


def normalizar_status_pedido(status):
    """Converte status antigos ou invalidos para um status valido."""
    if status == "Pendente":
        return "Pagamento pendente"
    if status in STATUS_PEDIDO:
        return status
    return "Pagamento pendente"


def obter_clientes_disponiveis():
    """Retorna os cadastros dos clientes para preencher o formulario de pedido."""
    return Cliente.query.order_by(Cliente.nome, Cliente.id).all()


def construir_catalogo_materiais(extra_stock=None):
    """Monta o catalogo de materiais disponiveis para a tela de pedido."""
    extra_stock = extra_stock or {}
    materiais = Material.query.all()
    materiais.sort(key=lambda item: (ORDEM_CATEGORIAS.get(item.categoria, 99), item.nome, item.largura_m))

    catalogo = {}

    for material in materiais:
        catalogo.setdefault(material.categoria, {})
        catalogo[material.categoria].setdefault(material.nome, [])
        catalogo[material.categoria][material.nome].append(
            {
                "id": material.id,
                "largura_m": round(material.largura_m, 2),
                "largura_formatada": material.largura_formatada,
                "bobinas": material.quantidade_bobinas,
                "metros_disponiveis": round(material.metros_disponiveis + extra_stock.get(material.id, 0), 2),
                "metros_disponiveis_formatados": formatar_metros(
                    round(material.metros_disponiveis + extra_stock.get(material.id, 0), 2)
                ),
            }
        )

    return catalogo


def dados_iniciais_formulario():
    """Retorna os valores padrao para um novo formulario de pedido."""
    return {
        "cliente_id": "",
        "categoria": "",
        "tipo": "",
        "largura": "",
        "altura": "",
        "unidade": "m",
        "adicionais": [],
        "quantidade": 1,
    }


def extrair_form_data_pedido():
    """Extrai e limpa os campos do formulario de pedido."""
    return {
        "adicionais": [
            {"material_id": material_id, "metros": metros}
            for material_id, metros in zip_longest(
                request.form.getlist("material_adicional_id"),
                request.form.getlist("material_adicional_metros"),
                fillvalue="",
            )
        ],
        "cliente_id": request.form.get("cliente_id", "").strip(),
        "categoria": request.form.get("categoria", "").strip(),
        "tipo": request.form.get("tipo", "").strip(),
        "largura": request.form.get("largura", "").strip(),
        "altura": request.form.get("altura", "").strip(),
        "unidade": request.form.get("unidade", "m").strip(),
        "quantidade": request.form.get("quantidade", "1").strip(),
    }


def form_data_do_pedido(pedido):
    """Converte um pedido existente para dados editaveis no formulario."""
    principal = obter_material_do_pedido(pedido)
    return {
        "adicionais": [
            {"material_id": str(item.material_id), "metros": item.quantidade_metros}
            for item in pedido.consumos if not item.principal
        ],
        "cliente_id": str(pedido.cliente_id) if pedido.cliente_id else "",
        "categoria": principal.categoria if principal else pedido.categoria,
        "tipo": principal.nome if principal else pedido.material_nome,
        "largura": f"{pedido.largura_pedido_m:.2f}",
        "altura": f"{pedido.altura_pedido_m:.2f}",
        "unidade": "m",
        "quantidade": pedido.quantidade,
    }


def obter_material_do_pedido(pedido):
    """Localiza o material usado por um pedido ja cadastrado."""
    principal = next((item.material for item in pedido.consumos if item.principal), None)
    if principal is not None:
        return principal
    return Material.query.filter_by(
        categoria=pedido.categoria,
        nome=pedido.material_nome,
        largura_m=pedido.largura_bobina_usada_m,
    ).first()


def obter_extra_stock_para_pedido(pedido):
    """Libera virtualmente o estoque do pedido durante sua propria edicao."""
    return {
        material.id: metros for material, metros in consumos_do_pedido(pedido)
    }


def renderizar_formulario_pedido(form_data, erro="", pedido=None):
    """Renderiza o formulario de criacao ou edicao de pedido."""
    extra_stock = obter_extra_stock_para_pedido(pedido) if pedido else {}
    catalogo = construir_catalogo_materiais(extra_stock=extra_stock)
    clientes = obter_clientes_disponiveis()

    return render_template(
        "pedidos/novo.html",
        materiais_adicionais=Material.query.order_by(Material.categoria, Material.nome, Material.id).all(),
        clientes=clientes,
        catalogo=catalogo,
        erro=erro,
        form_data=form_data,
        pedido=pedido,
        titulo_pagina="Editar Pedido" if pedido else "Novo Pedido",
        texto_submit="Salvar Alterações" if pedido else "Salvar Pedido",
        rota_submit=url_for("pedido.editar_pedido", id=pedido.id) if pedido else url_for("pedido.novo_pedido"),
    )


def processar_salvamento_pedido(form_data, pedido=None):
    try:
        resultado, erro = _processar_salvamento_pedido(form_data, pedido)
        if erro:
            db.session.rollback()
        return resultado, erro
    except SQLAlchemyError:
        db.session.rollback()
        return None, "Nao foi possivel salvar o pedido. Nenhum consumo foi aplicado."
    except Exception:
        db.session.rollback()
        raise


def _processar_salvamento_pedido(form_data, pedido=None):
    """Valida dados, calcula aproveitamento, atualiza estoque e salva pedido."""
    try:
        quantidade = int(form_data["quantidade"])
        largura_m = converter_para_metros(form_data["largura"], form_data["unidade"])
        altura_m = converter_para_metros(form_data["altura"], form_data["unidade"])
    except (TypeError, ValueError):
        quantidade = 0
        largura_m = 0
        altura_m = 0

    cliente_id = form_data["cliente_id"]
    manter_legado = pedido is not None and pedido.cliente_id is None and not cliente_id
    cliente = None
    if cliente_id:
        try:
            cliente = db.session.get(Cliente, int(cliente_id))
        except ValueError:
            pass
    if not cliente and not manter_legado:
        return None, "Selecione um cliente cadastrado válido."

    if (
        not form_data["categoria"]
        or not form_data["tipo"]
        or quantidade <= 0
        or not math.isfinite(largura_m)
        or not math.isfinite(altura_m)
        or largura_m <= 0
        or altura_m <= 0
    ):
        return None, "Preencha cliente, material, medidas e quantidade com valores válidos."

    extra_stock = obter_extra_stock_para_pedido(pedido) if pedido else {}
    variacoes = Material.query.filter_by(
        categoria=form_data["categoria"],
        nome=form_data["tipo"],
    ).all()

    sugestao = calcular_melhor_aproveitamento(
        variacoes,
        largura_m,
        altura_m,
        quantidade,
        extra_stock=extra_stock,
    )

    if not sugestao:
        return None, "Não há bobinas com largura e metragem suficientes para esse pedido."

    try:
        plano = planejar_consumos(
            sugestao["material"], sugestao["metros_consumidos"],
            form_data.get("adicionais", []), extra_stock,
        )
    except ValueError as erro:
        return None, str(erro)

    if pedido:
        consumos_anteriores = consumos_do_pedido(pedido)
        if not consumos_anteriores:
            return None, "Material do pedido antigo nao identificado. Regularize antes de editar."
        for material_anterior, metros_anteriores in consumos_anteriores:
            devolver_material(material_anterior, metros_anteriores)
            registrar_movimentacao(
                material_anterior, "entrada", metros_anteriores,
                session.get("usuario_id"), f"Estorno para edição do pedido #{pedido.id}",
            )
        pedido.consumos.clear()
        db.session.flush()

    for material, metros, principal in plano:
        if not consumir_material(material, metros):
            db.session.rollback()
            return None, "Nao foi possivel baixar o estoque de todos os materiais."

    area_total = round(largura_m * altura_m * quantidade, 2)

    if not pedido:
        pedido = Pedido()
        db.session.add(pedido)

    if cliente:
        if pedido.cliente_id != cliente.id:
            pedido.cliente_nome = cliente.nome
        pedido.cliente_id = cliente.id
    pedido.categoria = form_data["categoria"]
    pedido.material_nome = form_data["tipo"]
    pedido.largura_pedido_m = largura_m
    pedido.altura_pedido_m = altura_m
    pedido.quantidade = quantidade
    pedido.unidade_medida = form_data["unidade"]
    pedido.largura_bobina_usada_m = sugestao["largura_bobina"]
    pedido.orientacao = sugestao["orientacao"]
    pedido.metros_consumidos = sugestao["metros_consumidos"]
    pedido.area_total_m2 = area_total
    pedido.status = normalizar_status_pedido(pedido.status)

    db.session.flush()
    for material, metros, principal in plano:
        pedido.consumos.append(ConsumoMaterial(
            material=material, quantidade_metros=metros, principal=principal,
        ))
        registrar_movimentacao(
            material, "saida", metros,
            session.get("usuario_id"), f"Consumo do pedido #{pedido.id}",
        )
    db.session.commit()
    return pedido, ""


@pedido_bp.route("/pedidos")
@login_required
def lista_pedidos():
    """Exibe a lista de pedidos com filtros de busca."""
    pedidos = Pedido.query.order_by(Pedido.id.desc()).all()
    busca = request.args.get("busca", "").strip()
    filtro = request.args.get("filtro", "id").strip()
    status_busca = request.args.get("status", "").strip()
    termo = normalizar_busca(busca)
    mostrar_finalizados = filtro == "status"

    for pedido in pedidos:
        pedido.status = normalizar_status_pedido(pedido.status)

    if not mostrar_finalizados:
        pedidos = [pedido for pedido in pedidos if normalizar_status_pedido(pedido.status) != "Finalizado"]

    if filtro == "status":
        if status_busca:
            pedidos = [
                pedido
                for pedido in pedidos
                if normalizar_status_pedido(pedido.status) == status_busca
            ]
    elif termo:
        if filtro == "cliente":
            pedidos = [pedido for pedido in pedidos if termo in normalizar_busca(pedido.cliente_nome)]
        elif filtro == "material":
            pedidos = [
                pedido
                for pedido in pedidos
                if termo in normalizar_busca(pedido.categoria)
                or termo in normalizar_busca(pedido.material_nome)
                or any(
                    termo in normalizar_busca(item.material.nome)
                    or termo in normalizar_busca(item.material.categoria)
                    for item in pedido.consumos
                )
            ]
        else:
            pedidos = [pedido for pedido in pedidos if termo in normalizar_busca(pedido.id)]

    return render_template(
        "pedidos/lista.html",
        pedidos=pedidos,
        busca=busca,
        filtro=filtro,
        status_busca=status_busca,
        status_pedido=STATUS_PEDIDO,
    )


@pedido_bp.route("/pedidos/<int:id>/status", methods=["POST"])
@login_required
def atualizar_status_pedido(id):
    """Atualiza o status de um pedido existente."""
    pedido = Pedido.query.get_or_404(id)
    status = request.form.get("status", "").strip()

    try:
        resultado = atualizar_status_com_notificacao(pedido, status, usuario_id=session.get("usuario_id"))
        if resultado is not None:
            mensagens = {
                "registro_pendente": ("Pedido pronto para retirada. O resultado da notificacao nao foi salvo; confira o historico antes de tentar outro envio.", "erro"),
                "aceito": ("Pedido pronto para retirada. Notificação do WhatsApp disparada com sucesso! Aceita pela API; entrega ainda não confirmada.", "sucesso"),
                "desabilitado": ("Pedido pronto para retirada. O envio de notificações pelo WhatsApp está desativado.", "info"),
                "bloqueado_testing": ("Pedido pronto para retirada. Notificação bloqueada no ambiente de testes.", "info"),
                "sem_destinatario": ("Pedido pronto para retirada. Notificação não enviada: verifique o telefone cadastrado do cliente.", "erro"),
                "configuracao_invalida": ("Pedido pronto para retirada. Notificação não enviada: serviço de WhatsApp indisponível.", "erro"),
            }
            mensagem, categoria = mensagens.get(resultado.status, (
                "Pedido pronto para retirada. Não foi possível confirmar a notificação pelo WhatsApp.", "erro"))
            flash(mensagem, categoria)
    except ValueError as erro:
        flash(str(erro), "erro")

    return redirect(url_for("pedido.lista_pedidos"))


@pedido_bp.route("/pedidos/novo", methods=["GET", "POST"])
@login_required
def novo_pedido():
    """Exibe e processa o formulario de novo pedido."""
    form_data = dados_iniciais_formulario()

    if request.method == "POST":
        form_data = extrair_form_data_pedido()
        pedido, erro = processar_salvamento_pedido(form_data)
        if pedido:
            return redirect(url_for("pedido.detalhe_pedido", id=pedido.id))
        return renderizar_formulario_pedido(form_data, erro=erro)

    return renderizar_formulario_pedido(form_data)


@pedido_bp.route("/pedidos/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_pedido(id):
    """Exibe e processa o formulario de edicao de pedido."""
    pedido = Pedido.query.get_or_404(id)

    if request.method == "POST":
        form_data = extrair_form_data_pedido()
        pedido_atualizado, erro = processar_salvamento_pedido(form_data, pedido=pedido)
        if pedido_atualizado:
            return redirect(url_for("pedido.detalhe_pedido", id=pedido_atualizado.id))
        return renderizar_formulario_pedido(form_data, erro=erro, pedido=pedido)

    return renderizar_formulario_pedido(form_data_do_pedido(pedido), pedido=pedido)


@pedido_bp.route("/pedidos/<int:id>/cancelar", methods=["POST"])
@login_required
def cancelar_pedido(id):
    """Cancela pedidos ainda nao prontos, estornando o material reservado."""
    pedido = Pedido.query.get_or_404(id)
    if pedido.status in {"Pronto para retirada", "Finalizado"}:
        flash(
            "Pedidos prontos ou finalizados não podem ser cancelados: "
            "o material já foi utilizado e não pode retornar ao estoque.",
            "erro",
        )
        return redirect(url_for("pedido.detalhe_pedido", id=pedido.id))

    consumos = consumos_do_pedido(pedido)
    if not consumos:
        flash("Material do pedido antigo nao identificado. Cancelamento nao realizado.", "erro")
        return redirect(url_for("pedido.detalhe_pedido", id=pedido.id))
    try:
        for material, metros in consumos:
            devolver_material(material, metros)
            registrar_movimentacao(
                material, "entrada", metros,
                session.get("usuario_id"), f"Estorno por cancelamento do pedido #{pedido.id}",
            )
        db.session.delete(pedido)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        flash("Nao foi possivel cancelar o pedido. Nenhum estorno foi aplicado.", "erro")
        return redirect(url_for("pedido.detalhe_pedido", id=pedido.id))
    return redirect(url_for("pedido.lista_pedidos"))


@pedido_bp.route("/pedidos/<int:id>")
@login_required
def detalhe_pedido(id):
    """Exibe os detalhes calculados de um pedido."""
    pedido = Pedido.query.get_or_404(id)

    return render_template(
        "pedidos/detalhe.html",
        pedido=pedido,
        area_total=formatar_area(pedido.area_total_m2),
        metros_consumidos=formatar_metros(pedido.metros_consumidos),
        largura_bobina_usada=formatar_metros(pedido.largura_bobina_usada_m),
        largura_pedido=formatar_metros(pedido.largura_pedido_m),
        altura_pedido=formatar_metros(pedido.altura_pedido_m),
        criado_em=pedido.criado_em.strftime("%d/%m/%Y %H:%M"),
    )
