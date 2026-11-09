"""Rotas e operacoes de interface para estoque."""

from math import isfinite
from sqlalchemy.exc import IntegrityError

from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from database.db import db
from models.categoria_material import CategoriaMaterial
from models.material import Material
from services.constantes import METROS_POR_BOBINA
from services.estoque_service import ajustar_metros_disponiveis, listar_movimentacoes, registrar_entrada_estoque, registrar_movimentacao, remover_bobina
from services.material_service import buscar_material_por_codigo_barras, normalizar_nome
from controllers.auth_required import login_required, admin_required

estoque_bp = Blueprint("estoque", __name__)

ORDEM_CATEGORIAS = {
    "Adesivo": 1,
    "Lona": 2,
    "Tecido": 3,
}


def construir_secoes_estoque(busca="", abaixo_minimo=False):
    """Agrupa materiais por categoria para exibicao na tela de estoque."""
    materiais = Material.query.all()

    if busca:
        busca_normalizada = normalizar_nome(busca)

        materiais = [
            material
            for material in materiais
            if (
                busca_normalizada in normalizar_nome(material.nome)
                or busca in (material.codigo_barras or "")
            )
        ]
    if abaixo_minimo:
        materiais = [material for material in materiais if material.abaixo_estoque_minimo]

    materiais.sort(key=lambda item: (ORDEM_CATEGORIAS.get(item.categoria, 99), item.nome, item.largura_m))

    categorias = [categoria.nome for categoria in CategoriaMaterial.query.order_by(CategoriaMaterial.nome).all()]
    for material in materiais:
        if material.categoria not in categorias:
            categorias.append(material.categoria)

    secoes = {categoria: [] for categoria in categorias}

    for material in materiais:
        secoes.setdefault(material.categoria, [])
        secoes[material.categoria].append(
            {
                "estoque_minimo": f"{material.estoque_minimo:.2f}",
                "estoque_minimo_formatado": material.estoque_minimo_formatado,
                "abaixo_minimo": material.abaixo_estoque_minimo,
                "id": material.id,
                "nome": material.nome,
                "codigo_barras": material.codigo_barras,
                "largura": material.largura_formatada,
                "bobinas": material.quantidade_bobinas,
                "metros_restantes_valor": f"{material.metros_disponiveis:.2f}",
                "metros_restantes": material.metros_disponiveis_formatados,
            }
        )

    resultado = [
    {"categoria": categoria, "itens": itens}
    for categoria, itens in sorted(
        secoes.items(),
        key=lambda item: ORDEM_CATEGORIAS.get(item[0], 99)
    )
]

    if busca or abaixo_minimo:
       resultado = [
        secao
        for secao in resultado
        if secao["itens"]
       ]

    return resultado


@estoque_bp.route("/estoque")
@login_required
def lista_estoque():
    """Exibe a tela principal de estoque."""
    busca = request.args.get("busca", "").strip()

    abaixo_minimo = request.args.get("abaixo_minimo") == "1"
    secoes = construir_secoes_estoque(busca, abaixo_minimo=abaixo_minimo)

    return render_template(
        "estoque/lista.html",
        secoes=secoes,
        busca=busca,
        abaixo_minimo=abaixo_minimo,
    )

@estoque_bp.route("/estoque/categoria/nova", methods=["POST"])
@admin_required
def nova_categoria():
    """Cadastra uma nova categoria de material."""
    nome = request.form.get("nome", "").strip()

    if nome:
        categoria = next(
            (
                categoria
                for categoria in CategoriaMaterial.query.all()
                if normalizar_nome(categoria.nome) == normalizar_nome(nome)
            ),
            None,
        )
        if categoria:
            flash("Esse tipo de material já existe.", "erro")
        else:
            db.session.add(CategoriaMaterial(nome=nome))
            db.session.commit()
            flash("Tipo de material cadastrado com sucesso.", "sucesso")

    return redirect(url_for("estoque.lista_estoque"))


@estoque_bp.route("/estoque/novo", methods=["GET", "POST"])
@admin_required
def novo_estoque():
    """Exibe e processa o formulario de cadastro de material."""
    erro = ""
    categorias = [
        categoria.nome
        for categoria in CategoriaMaterial.query.order_by(CategoriaMaterial.nome).all()
    ]

    if request.method == "POST":
        categoria = request.form.get("categoria", "").strip()
        nome = request.form.get("nome", "").strip()
        codigo_barras = request.form.get("codigo_barras", "").strip()
        largura_texto = request.form.get("largura_m", "").strip().replace(",", ".")
        unidades_texto = request.form.get("unidades", "1").strip()

        try:
            largura_m = float(largura_texto)
            unidades = int(unidades_texto)
            estoque_minimo = validar_estoque_minimo(request.form.get("estoque_minimo", "0"))
        except ValueError:
            largura_m = 0
            unidades = 0
            estoque_minimo = 0

        if (
            not categoria
            or not nome
            or not codigo_barras
            or not isfinite(largura_m)
            or largura_m <= 0
            or unidades <= 0
        ):
            erro = (
                "Preencha tipo, nome, código de barras, "
                "largura, unidades e estoque mínimo com valores válidos."
            )
        else:
            codigo_existente = Material.query.filter_by(
                codigo_barras=codigo_barras
            ).first()

            if codigo_existente:
                erro = "Esse código de barras já está cadastrado."
            else:
                material = next(
                    (
                        item
                        for item in Material.query.filter_by(categoria=categoria).all()
                        if normalizar_nome(item.nome) == normalizar_nome(nome)
                        and round(item.largura_m, 2) == round(largura_m, 2)
                    ),
                    None,
                )

                if material:
                    erro = "Essa variação de material já existe nesse tipo e largura."
                else:
                    material = Material(
                        categoria=categoria,
                        nome=nome,
                        largura_m=largura_m,
                        codigo_barras=codigo_barras,
                        estoque_minimo=estoque_minimo,
                    )

                    db.session.add(material)
                    db.session.flush()

                    registrar_entrada_estoque(
                        material, unidades, usuario_id=session.get("usuario_id"),
                        motivo="Estoque inicial no cadastro do material",
                    )
                    db.session.commit()

                    flash("Material cadastrado com sucesso.", "sucesso")
                    return redirect(url_for("estoque.lista_estoque"))

    return render_template(
        "estoque/novo.html",
        erro=erro,
        categorias=categorias,
    )


@estoque_bp.route("/estoque/material/<int:material_id>/adicionar-unidade", methods=["POST"])
@admin_required
def adicionar_unidade(material_id):
    """Adiciona uma bobina ao material informado."""
    material = Material.query.get_or_404(material_id)
    registrar_entrada_estoque(
        material, 1, usuario_id=session.get("usuario_id"),
        motivo="Adição manual de bobina",
    )
    db.session.commit()
    return redirect(url_for("estoque.lista_estoque"))


@estoque_bp.route("/estoque/material/<int:material_id>/remover-unidade", methods=["POST"])
@admin_required
def remover_unidade(material_id):
    """Remove uma bobina do material informado."""
    material = Material.query.get_or_404(material_id)
    metros_antes = material.metros_disponiveis
    if remover_bobina(material):
        registrar_movimentacao(
            material, "saida", metros_antes - material.metros_disponiveis,
            session.get("usuario_id"), "Remoção manual de bobina", bobinas=1,
        )
    db.session.commit()
    return redirect(url_for("estoque.lista_estoque"))


@estoque_bp.route("/estoque/material/<int:material_id>/editar-metros", methods=["POST"])
@admin_required
def editar_metros(material_id):
    """Atualiza manualmente a metragem disponivel de um material."""
    material = Material.query.get_or_404(material_id)
    metros_texto = request.form.get("metros_disponiveis", "").strip().replace(",", ".")

    try:
        metros_disponiveis = float(metros_texto)
    except ValueError:
        flash("Informe uma metragem valida.", "erro")
        return redirect(url_for("estoque.lista_estoque"))

    if not isfinite(metros_disponiveis) or metros_disponiveis < 0:
        flash("Informe uma metragem finita maior ou igual a zero.", "erro")
        return redirect(url_for("estoque.lista_estoque"))

    capacidade_total = material.quantidade_bobinas * METROS_POR_BOBINA
    if metros_disponiveis > capacidade_total:
        flash("A metragem disponível não pode ser maior que a soma das bobinas cadastradas.", "erro")
        return redirect(url_for("estoque.lista_estoque"))

    metros_antes = material.metros_disponiveis
    ajustar_metros_disponiveis(material, metros_disponiveis)
    diferenca = round(material.metros_disponiveis - metros_antes, 2)
    if diferenca:
        registrar_movimentacao(
            material, "ajuste", abs(diferenca), session.get("usuario_id"),
            f"Ajuste manual: {metros_antes:.2f} m → {material.metros_disponiveis:.2f} m",
        )
    db.session.commit()
    return redirect(url_for("estoque.lista_estoque"))


@estoque_bp.route("/estoque/material/<int:material_id>/excluir", methods=["POST"])
@admin_required
def excluir_material(material_id):
    """Exclui um material cadastrado no estoque."""
    material = Material.query.get_or_404(material_id)
    descricao_material = f"{material.nome} ({material.largura_formatada})"

    if material.movimentacoes.first():
        flash("Material com histórico de movimentações não pode ser excluído.", "erro")
        return redirect(url_for("estoque.lista_estoque"))

    db.session.delete(material)
    db.session.commit()
    flash(f'Material "{descricao_material}" excluído com sucesso.', "sucesso")

    return redirect(url_for("estoque.lista_estoque"))


@estoque_bp.route("/estoque/entrada", methods=["POST"])
@login_required
def entrada_estoque():
    """Processa a entrada de material no estoque via codigo de barras."""
    codigo_barras = request.form.get("codigo_barras", "").strip()
    quantidade_texto = request.form.get("quantidade_bobinas", "1").strip()
    motivo = request.form.get("motivo", "").strip() or "Entrada via código de barras"

    if not codigo_barras:
        flash("Informe o código de barras do material.", "erro")
        return redirect(url_for("estoque.lista_estoque"))

    try:
        quantidade_bobinas = int(quantidade_texto)
    except ValueError:
        quantidade_bobinas = 0

    if quantidade_bobinas <= 0:
        flash("A quantidade de bobinas deve ser maior que zero.", "erro")
        return redirect(url_for("estoque.lista_estoque"))

    material = buscar_material_por_codigo_barras(codigo_barras)
    if not material:
        flash(f'Material com código de barras "{codigo_barras}" não encontrado.', "erro")
        return redirect(url_for("estoque.lista_estoque"))

    usuario_id = session.get("usuario_id")
    registrar_entrada_estoque(
        material=material,
        quantidade_bobinas=quantidade_bobinas,
        usuario_id=usuario_id,
        motivo=motivo,
    )
    db.session.commit()

    flash(
        f"Entrada de {quantidade_bobinas} bobina(s) registrada com sucesso para {material.nome} ({material.largura_formatada}).",
        "sucesso",
    )
    return redirect(url_for("estoque.lista_estoque"))

@estoque_bp.route("/estoque/movimentacoes")
@login_required
def movimentacoes():
    """Exibe o histórico de movimentações do estoque."""

    tipo = request.args.get("tipo", "").strip().lower()
    material_id_texto = request.args.get("material_id", "").strip()

    material_id = None

    if material_id_texto:
        try:
            material_id = int(material_id_texto)
        except ValueError:
            material_id = None

    tipos_validos = {"entrada", "saida", "ajuste"}

    if tipo not in tipos_validos:
        tipo = None

    movimentacoes_lista = listar_movimentacoes(
        limite=100,
        material_id=material_id,
        tipo=tipo,
    )

    materiais = Material.query.order_by(Material.nome, Material.largura_m).all()

    return render_template(
        "estoque/movimentacoes.html",
        movimentacoes=movimentacoes_lista,
        materiais=materiais,
        filtro_tipo=tipo,
        filtro_material_id=material_id,
    )

@estoque_bp.route("/estoque/api/material/codigo/<codigo_barras>")
@login_required
def api_material_por_codigo(codigo_barras):
    """Retorna os dados de um material pelo codigo de barras em formato JSON."""
    material = buscar_material_por_codigo_barras(codigo_barras)

    if not material:
        return jsonify({"erro": "Material não encontrado"}), 404

    return jsonify({
        "id": material.id,
        "nome": material.nome,
        "categoria": material.categoria,
        "largura": material.largura_formatada,
        "metros_disponiveis": material.metros_disponiveis_formatados,
        "codigo_barras": material.codigo_barras,
    })


def validar_estoque_minimo(valor):
    """Aceita um limite finito e nao negativo, em metros."""
    minimo = float(str(valor).strip().replace(",", "."))
    if not isfinite(minimo) or minimo < 0:
        raise ValueError("Informe um estoque minimo finito maior ou igual a zero.")
    return round(minimo, 2)


@estoque_bp.route("/estoque/material/<int:material_id>/estoque-minimo", methods=["POST"])
@admin_required
def editar_estoque_minimo(material_id):
    material = Material.query.get_or_404(material_id)
    try:
        minimo = validar_estoque_minimo(request.form.get("estoque_minimo", ""))
    except ValueError:
        flash("Informe um estoque minimo finito maior ou igual a zero.", "erro")
        return redirect(url_for("estoque.lista_estoque"))
    material.estoque_minimo = minimo
    db.session.commit()
    flash("Estoque minimo atualizado com sucesso.", "sucesso")
    return redirect(url_for("estoque.lista_estoque"))


@estoque_bp.route("/estoque/material/<int:material_id>/codigo-barras", methods=["POST"])
@admin_required
def editar_codigo_barras(material_id):
    """Regulariza a identificacao sem alterar bobinas ou movimentacoes."""
    material = Material.query.get_or_404(material_id)
    codigo = request.form.get("codigo_barras", "").strip()
    if not codigo or len(codigo) > 50 or any(ord(c) < 32 or ord(c) == 127 for c in codigo):
        flash("Informe um código de barras válido, com até 50 caracteres.", "erro")
        return redirect(url_for("estoque.lista_estoque"))
    existente = Material.query.filter(
        Material.codigo_barras == codigo, Material.id != material.id,
    ).first()
    if existente:
        flash("Esse código de barras já está cadastrado em outro material.", "erro")
        return redirect(url_for("estoque.lista_estoque"))
    material.codigo_barras = codigo
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Não foi possível salvar: código de barras já utilizado. Atualize a página.", "erro")
        return redirect(url_for("estoque.lista_estoque"))
    flash("Código de barras atualizado com sucesso.", "sucesso")
    return redirect(url_for("estoque.lista_estoque"))
