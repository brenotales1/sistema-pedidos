from flask import Blueprint, flash, redirect, render_template, request, url_for

from database.db import db
from models.categoria_material import CategoriaMaterial
from models.material import Material
from services.constantes import METROS_POR_BOBINA
from services.estoque_service import adicionar_bobina, ajustar_metros_disponiveis, remover_bobina
from services.material_service import normalizar_nome

estoque_bp = Blueprint("estoque", __name__)

ORDEM_CATEGORIAS = {
    "Adesivo": 1,
    "Lona": 2,
    "Tecido": 3,
}


def construir_secoes_estoque():
    materiais = Material.query.all()
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
                "id": material.id,
                "nome": material.nome,
                "largura": material.largura_formatada,
                "bobinas": material.quantidade_bobinas,
                "metros_restantes_valor": f"{material.metros_disponiveis:.2f}",
                "metros_restantes": material.metros_disponiveis_formatados,
            }
        )

    return [
        {"categoria": categoria, "itens": itens}
        for categoria, itens in sorted(secoes.items(), key=lambda item: ORDEM_CATEGORIAS.get(item[0], 99))
    ]


@estoque_bp.route("/estoque")
def lista_estoque():
    secoes = construir_secoes_estoque()
    return render_template("estoque/lista.html", secoes=secoes)


@estoque_bp.route("/estoque/categoria/nova", methods=["POST"])
def nova_categoria():
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
def novo_estoque():
    erro = ""
    categorias = [categoria.nome for categoria in CategoriaMaterial.query.order_by(CategoriaMaterial.nome).all()]

    if request.method == "POST":
        categoria = request.form.get("categoria", "").strip()
        nome = request.form.get("nome", "").strip()
        largura_texto = request.form.get("largura_m", "").strip().replace(",", ".")
        unidades_texto = request.form.get("unidades", "1").strip()

        try:
            largura_m = float(largura_texto)
            unidades = int(unidades_texto)
        except ValueError:
            largura_m = 0
            unidades = 0

        if not categoria or not nome or largura_m <= 0 or unidades <= 0:
            erro = "Preencha tipo, nome, largura e unidades com valores válidos."
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
                material = Material(categoria=categoria, nome=nome, largura_m=largura_m)
                db.session.add(material)
                db.session.flush()

                adicionar_bobina(material, unidades)
                db.session.commit()
                flash("Material cadastrado com sucesso.", "sucesso")
                return redirect(url_for("estoque.lista_estoque"))

    return render_template("estoque/novo.html", erro=erro, categorias=categorias)


@estoque_bp.route("/estoque/material/<int:material_id>/adicionar-unidade", methods=["POST"])
def adicionar_unidade(material_id):
    material = Material.query.get_or_404(material_id)
    adicionar_bobina(material, 1)
    db.session.commit()
    return redirect(url_for("estoque.lista_estoque"))


@estoque_bp.route("/estoque/material/<int:material_id>/remover-unidade", methods=["POST"])
def remover_unidade(material_id):
    material = Material.query.get_or_404(material_id)
    remover_bobina(material)
    db.session.commit()
    return redirect(url_for("estoque.lista_estoque"))


@estoque_bp.route("/estoque/material/<int:material_id>/editar-metros", methods=["POST"])
def editar_metros(material_id):
    material = Material.query.get_or_404(material_id)
    metros_texto = request.form.get("metros_disponiveis", "").strip().replace(",", ".")

    try:
        metros_disponiveis = float(metros_texto)
    except ValueError:
        metros_disponiveis = material.metros_disponiveis

    capacidade_total = material.quantidade_bobinas * METROS_POR_BOBINA
    if metros_disponiveis > capacidade_total:
        flash("A metragem disponível não pode ser maior que a soma das bobinas cadastradas.", "erro")
        return redirect(url_for("estoque.lista_estoque"))

    ajustar_metros_disponiveis(material, metros_disponiveis)
    db.session.commit()
    return redirect(url_for("estoque.lista_estoque"))


@estoque_bp.route("/estoque/material/<int:material_id>/excluir", methods=["POST"])
def excluir_material(material_id):
    material = Material.query.get_or_404(material_id)
    descricao_material = f"{material.nome} ({material.largura_formatada})"

    db.session.delete(material)
    db.session.commit()
    flash(f'Material "{descricao_material}" excluído com sucesso.', "sucesso")

    return redirect(url_for("estoque.lista_estoque"))
