"""Rotas e operacoes de interface para pedidos."""

from flask import Blueprint, redirect, render_template, request, url_for

from database.db import db
from models.cliente import Cliente
from models.material import Material
from models.pedido import Pedido
from services.estoque_service import consumir_material, devolver_material
from services.pedido_service import (
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

STATUS_PEDIDO = [
    "Pagamento pendente",
    "Aguardando produção",
    "Pronto para retirada",
    "Finalizado",
]


def normalizar_status_pedido(status):
    """Converte status antigos ou invalidos para um status valido."""
    if status == "Pendente":
        return "Pagamento pendente"
    if status in STATUS_PEDIDO:
        return status
    return "Pagamento pendente"


def obter_clientes_disponiveis():
    """Retorna os nomes dos clientes para preencher o formulario de pedido."""
    return [cliente.nome for cliente in Cliente.query.order_by(Cliente.nome).all()]


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
        "cliente": "",
        "categoria": "",
        "tipo": "",
        "largura": "",
        "altura": "",
        "unidade": "m",
        "quantidade": 1,
    }


def extrair_form_data_pedido():
    """Extrai e limpa os campos do formulario de pedido."""
    return {
        "cliente": request.form.get("cliente", "").strip(),
        "categoria": request.form.get("categoria", "").strip(),
        "tipo": request.form.get("tipo", "").strip(),
        "largura": request.form.get("largura", "").strip(),
        "altura": request.form.get("altura", "").strip(),
        "unidade": request.form.get("unidade", "m").strip(),
        "quantidade": request.form.get("quantidade", "1").strip(),
    }


def form_data_do_pedido(pedido):
    """Converte um pedido existente para dados editaveis no formulario."""
    return {
        "cliente": pedido.cliente_nome,
        "categoria": pedido.categoria,
        "tipo": pedido.material_nome,
        "largura": f"{pedido.largura_pedido_m:.2f}",
        "altura": f"{pedido.altura_pedido_m:.2f}",
        "unidade": "m",
        "quantidade": pedido.quantidade,
    }


def obter_material_do_pedido(pedido):
    """Localiza o material usado por um pedido ja cadastrado."""
    return Material.query.filter_by(
        categoria=pedido.categoria,
        nome=pedido.material_nome,
        largura_m=pedido.largura_bobina_usada_m,
    ).first()


def obter_extra_stock_para_pedido(pedido):
    """Libera virtualmente o estoque do pedido durante sua propria edicao."""
    material = obter_material_do_pedido(pedido)
    if not material:
        return {}
    return {material.id: pedido.metros_consumidos}


def renderizar_formulario_pedido(form_data, erro="", pedido=None):
    """Renderiza o formulario de criacao ou edicao de pedido."""
    extra_stock = obter_extra_stock_para_pedido(pedido) if pedido else {}
    catalogo = construir_catalogo_materiais(extra_stock=extra_stock)
    clientes = obter_clientes_disponiveis()

    return render_template(
        "pedidos/novo.html",
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
    """Valida dados, calcula aproveitamento, atualiza estoque e salva pedido."""
    try:
        quantidade = int(form_data["quantidade"])
        largura_m = converter_para_metros(form_data["largura"], form_data["unidade"])
        altura_m = converter_para_metros(form_data["altura"], form_data["unidade"])
    except (TypeError, ValueError):
        quantidade = 0
        largura_m = 0
        altura_m = 0

    if (
        not form_data["cliente"]
        or not form_data["categoria"]
        or not form_data["tipo"]
        or quantidade <= 0
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

    if pedido:
        material_anterior = obter_material_do_pedido(pedido)
        if material_anterior:
            devolver_material(material_anterior, pedido.metros_consumidos)

    if not consumir_material(sugestao["material"], sugestao["metros_consumidos"]):
        db.session.rollback()
        return None, "Não foi possível baixar o estoque desse material."

    area_total = round(largura_m * altura_m * quantidade, 2)

    if not pedido:
        pedido = Pedido()
        db.session.add(pedido)

    pedido.cliente_nome = form_data["cliente"]
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

    db.session.commit()
    return pedido, ""


@pedido_bp.route("/pedidos")
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
                if termo in normalizar_busca(pedido.categoria) or termo in normalizar_busca(pedido.material_nome)
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
def atualizar_status_pedido(id):
    """Atualiza o status de um pedido existente."""
    pedido = Pedido.query.get_or_404(id)
    status = request.form.get("status", "").strip()

    if status in STATUS_PEDIDO:
        pedido.status = status
        db.session.commit()

    return redirect(url_for("pedido.lista_pedidos"))


@pedido_bp.route("/pedidos/novo", methods=["GET", "POST"])
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
def cancelar_pedido(id):
    """Cancela um pedido e devolve sua metragem ao estoque."""
    pedido = Pedido.query.get_or_404(id)
    material = obter_material_do_pedido(pedido)

    if material:
        devolver_material(material, pedido.metros_consumidos)

    db.session.delete(pedido)
    db.session.commit()
    return redirect(url_for("pedido.lista_pedidos"))


@pedido_bp.route("/pedidos/<int:id>")
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
