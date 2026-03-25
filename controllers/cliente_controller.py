from flask import Blueprint, render_template

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/clientes")
def lista_clientes():

    clientes = [
        {"nome":"João","telefone":"9999-9999","empresa":"Loja X"},
        {"nome":"Maria","telefone":"8888-8888","empresa":"Gráfica"}
    ]

    return render_template("clientes/lista.html", clientes=clientes)