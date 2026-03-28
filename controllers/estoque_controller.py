from flask import Blueprint, render_template

estoque_bp = Blueprint("estoque", __name__)

@estoque_bp.route("/estoque")
def lista_estoque():

    materiais = [
        {"material":"Adesivo","disponivel":"45 m²","perda":"10%","alerta":"baixo"},
        {"material":"Lona","disponivel":"120 m²","perda":"5%","alerta":"ok"},
        {"material":"Tecido","disponivel":"30 m²","perda":"12%","alerta":"baixo"}
    ]

    return render_template("estoque/lista.html", materiais=materiais)

@estoque_bp.route("/estoque/novo")
def novo_estoque():
    return render_template("estoque/novo.html")