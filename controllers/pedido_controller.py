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