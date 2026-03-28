from flask import Blueprint, render_template

cliente_bp = Blueprint("cliente", __name__)

@cliente_bp.route("/clientes")
def lista_clientes():

    clientes = [
    {"id":1,"nome":"João","telefone":"9999-9999","empresa":"Loja X"},
    {"id":2,"nome":"Maria","telefone":"8888-8888","empresa":"Gráfica"}
    ]

    return render_template("clientes/lista.html", clientes=clientes)


@cliente_bp.route("/clientes/novo")
def novo_cliente():
    return render_template("clientes/novo.html")

@cliente_bp.route("/clientes/<int:id>/editar")
def editar_cliente(id):

    cliente = {
        "id": id,
        "nome": "João",
        "telefone": "9999-9999",
        "empresa": "Loja X"
    }

    return render_template("clientes/editar.html", cliente=cliente)