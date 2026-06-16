"""Rotas e operacoes de interface para clientes."""

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from database.db import db
from models.cliente import Cliente

cliente_bp = Blueprint("cliente", __name__)


def extrair_form_data_cliente(fonte):
    """Extrai e limpa os campos de cliente enviados pela interface."""
    return {
        "nome": fonte.get("nome", "").strip(),
        "telefone": fonte.get("telefone", "").strip(),
        "empresa": fonte.get("empresa", "").strip(),
    }


def preencher_cliente(cliente, form_data):
    """Preenche um objeto Cliente com dados ja validados."""
    cliente.nome = form_data["nome"]
    cliente.telefone = form_data["telefone"] or None
    cliente.empresa = form_data["empresa"] or None


def validar_cliente(form_data):
    """Valida os campos obrigatorios do cadastro de cliente."""
    if not form_data["nome"]:
        return "Informe o nome do cliente."

    return ""


@cliente_bp.route("/clientes")
def lista_clientes():
    """Exibe a listagem de clientes cadastrados."""
    clientes = Cliente.query.order_by(Cliente.nome).all()
    return render_template("clientes/lista.html", clientes=clientes)


@cliente_bp.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    """Exibe e processa o formulario de cadastro de cliente."""
    form_data = {"nome": "", "telefone": "", "empresa": ""}

    if request.method == "POST":
        form_data = extrair_form_data_cliente(request.form)
        erro = validar_cliente(form_data)

        if erro:
            return render_template("clientes/novo.html", erro=erro, form_data=form_data)

        cliente = Cliente()
        preencher_cliente(cliente, form_data)
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for("cliente.lista_clientes"))

    return render_template("clientes/novo.html", form_data=form_data)


@cliente_bp.route("/clientes/<int:id>/editar", methods=["GET", "POST"])
def editar_cliente(id):
    """Exibe e processa o formulario de edicao de cliente."""
    cliente = Cliente.query.get_or_404(id)
    form_data = {
        "nome": cliente.nome,
        "telefone": cliente.telefone or "",
        "empresa": cliente.empresa or "",
    }

    if request.method == "POST":
        form_data = extrair_form_data_cliente(request.form)
        erro = validar_cliente(form_data)

        if erro:
            return render_template("clientes/editar.html", cliente=cliente, erro=erro, form_data=form_data)

        preencher_cliente(cliente, form_data)
        db.session.commit()
        return redirect(url_for("cliente.lista_clientes"))

    return render_template("clientes/editar.html", cliente=cliente, form_data=form_data)


@cliente_bp.route("/clientes/rapido", methods=["POST"])
def criar_cliente_rapido():
    """Cria um cliente por requisicao JSON a partir do formulario de pedido."""
    dados = request.get_json(silent=True) or {}
    form_data = extrair_form_data_cliente(dados)
    erro = validar_cliente(form_data)

    if erro:
        return jsonify({"erro": erro}), 400

    cliente = Cliente()
    preencher_cliente(cliente, form_data)
    db.session.add(cliente)
    db.session.commit()

    return jsonify({"id": cliente.id, "nome": cliente.nome})
