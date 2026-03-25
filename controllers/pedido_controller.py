from flask import Blueprint, render_template

pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route("/pedidos")
def lista_pedidos():

    pedidos = [
        {"id":12,"cliente":"João","material":"Adesivo","status":"Pendente","valor":120},
        {"id":13,"cliente":"Maria","material":"Lona","status":"Produção","valor":300},
        {"id":14,"cliente":"Pedro","material":"ACM","status":"Finalizado","valor":500}
    ]

    return render_template("pedidos/lista.html", pedidos=pedidos)

@pedido_bp.route("/pedidos/novo")
def novo_pedido():
    return render_template("pedidos/novo.html")


@pedido_bp.route("/pedidos/<int:id>")
def detalhe_pedido(id):

    pedido = {
        "id":12,
        "cliente":"João da Silva",
        "status":"Pendente",
        "data":"19/03/2026",
        "material":"Adesivo",
        "tipo":"Blackout",
        "largura":2.00,
        "altura":1.50,
        "unidade":"m",
        "quantidade":3,
        "preco_m2":80,
        "area":3.00,
        "total":720
    }

    return render_template("pedidos/detalhe.html", pedido=pedido)