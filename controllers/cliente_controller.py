"""Rotas e operacoes de interface para clientes."""

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from database.db import db
from models.cliente import Cliente
from controllers.auth_required import login_required

cliente_bp = Blueprint("cliente", __name__)


def extrair_form_data_cliente(fonte):
    """Extrai e limpa os campos de cliente enviados pela interface."""
    return {
        "nome": str(fonte.get("nome") or "").strip(),
        "telefone": str(fonte.get("telefone") or "").strip(),
        "empresa": str(fonte.get("empresa") or "").strip(),
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

    for campo, limite in (("nome", 120), ("telefone", 20), ("empresa", 120)):
        if len(form_data[campo]) > limite:
            return f"O campo {campo} deve ter no maximo {limite} caracteres."

    return ""


@cliente_bp.route("/clientes")
@login_required
def lista_clientes():
    """Exibe a listagem de clientes cadastrados."""
    clientes = Cliente.query.order_by(Cliente.nome).all()
    return render_template("clientes/lista.html", clientes=clientes)


@cliente_bp.route("/clientes/novo", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
def criar_cliente_rapido():
    """Cria um cliente por requisicao JSON a partir do formulario de pedido."""
    dados = request.get_json(silent=True) or {}
    if not isinstance(dados, dict) or any(
        valor is not None and not isinstance(valor, str)
        for valor in (dados.get("nome"), dados.get("telefone"), dados.get("empresa"))
    ):
        return jsonify({"erro": "Informe nome, telefone e empresa como texto."}), 400
    form_data = extrair_form_data_cliente(dados)
    erro = validar_cliente(form_data)

    if erro:
        return jsonify({"erro": erro}), 400

    cliente = Cliente()
    preencher_cliente(cliente, form_data)
    db.session.add(cliente)
    db.session.commit()

    return jsonify({"id": cliente.id, "nome": cliente.nome})
