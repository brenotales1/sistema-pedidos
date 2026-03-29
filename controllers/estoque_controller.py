from flask import Blueprint, redirect, render_template, request, url_for

from database.db import db
from models.material import Material
from services.estoque_service import adicionar_rolo, remover_rolo

estoque_bp = Blueprint("estoque", __name__)

ORDEM_CATEGORIAS = {
    "Adesivo": 1,
    "Lona": 2,
    "Tecido": 3,
}


def construir_secoes_estoque():
    materiais = Material.query.all()
    materiais.sort(key=lambda item: (ORDEM_CATEGORIAS.get(item.categoria, 99), item.nome, item.largura_m))

    secoes = {}

    for material in materiais:
        secoes.setdefault(material.categoria, [])
        secoes[material.categoria].append(
            {
                "id": material.id,
                "nome": material.nome,
                "largura": material.largura_formatada,
                "rolos": material.quantidade_rolos,
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


@estoque_bp.route("/estoque/novo", methods=["GET", "POST"])
def novo_estoque():
    erro = ""

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
            material = Material.query.filter_by(
                categoria=categoria,
                nome=nome,
                largura_m=largura_m,
            ).first()

            if not material:
                material = Material(categoria=categoria, nome=nome, largura_m=largura_m)
                db.session.add(material)
                db.session.flush()

            adicionar_rolo(material, unidades)
            db.session.commit()
            return redirect(url_for("estoque.lista_estoque"))

    return render_template("estoque/novo.html", erro=erro)


@estoque_bp.route("/estoque/material/<int:material_id>/adicionar-unidade", methods=["POST"])
def adicionar_unidade(material_id):
    material = Material.query.get_or_404(material_id)
    adicionar_rolo(material, 1)
    db.session.commit()
    return redirect(url_for("estoque.lista_estoque"))


@estoque_bp.route("/estoque/material/<int:material_id>/remover-unidade", methods=["POST"])
def remover_unidade(material_id):
    material = Material.query.get_or_404(material_id)
    remover_rolo(material)
    db.session.commit()
    return redirect(url_for("estoque.lista_estoque"))
