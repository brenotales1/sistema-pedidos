"""Testes automatizados para o modulo de gerenciamento de clientes."""

import unittest
from app import create_app
from database.db import db
from models.cliente import Cliente
from models.usuario import Usuario


class ClientesTestCase(unittest.TestCase):
    """Casos de teste para cadastro, edicao e validacoes de clientes."""

    def setUp(self):
        """Configura banco em memoria com usuario autenticado."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            user = Usuario.query.filter_by(email="func@sistema.com").first()
            if not user:
                user = Usuario(nome="Funcionario", email="func@sistema.com", perfil="funcionario")
                user.definir_senha("123456")
                db.session.add(user)

            cli = Cliente.query.filter_by(nome="Cliente Inicial").first()
            if not cli:
                cli = Cliente(nome="Cliente Inicial", telefone="11988888888", empresa="Empresa Alpha")
                db.session.add(cli)
            db.session.commit()

        self.client.post("/login", data={"email": "func@sistema.com", "senha": "123456"})

    def tearDown(self):
        """Limpa o banco ao final do teste."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_listagem_clientes(self):
        """Listagem de clientes exibe os dados cadastrados."""
        response = self.client.get("/clientes")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cliente Inicial".encode("utf-8"), response.data)
        self.assertIn("Empresa Alpha".encode("utf-8"), response.data)

    def test_cadastro_novo_cliente_valido(self):
        """Cadastro de novo cliente com dados validos e persistido."""
        response = self.client.post(
            "/clientes/novo",
            data={"nome": "Novo Cliente Silva", "telefone": "16999998888", "empresa": "Loja Silva"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            cli = Cliente.query.filter_by(nome="Novo Cliente Silva").first()
            self.assertIsNotNone(cli)
            self.assertEqual(cli.telefone, "16999998888")
            self.assertEqual(cli.empresa, "Loja Silva")

    def test_cadastro_cliente_nome_obrigatorio(self):
        """Cadastro sem informar nome exibe mensagem de erro de validacao."""
        response = self.client.post(
            "/clientes/novo",
            data={"nome": "", "telefone": "16999998888", "empresa": "Loja Silva"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Informe o nome do cliente".encode("utf-8"), response.data)

    def test_edicao_cliente(self):
        """Edicao de dados do cliente altera o registro existente."""
        with self.app.app_context():
            cli = Cliente.query.filter_by(nome="Cliente Inicial").first()
            cli_id = cli.id

        response = self.client.post(
            f"/clientes/{cli_id}/editar",
            data={"nome": "Cliente Alterado", "telefone": "11777777777", "empresa": "Empresa Beta"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            cli_atualizado = Cliente.query.get(cli_id)
            self.assertEqual(cli_atualizado.nome, "Cliente Alterado")
            self.assertEqual(cli_atualizado.empresa, "Empresa Beta")

    def test_cadastro_rapido_cliente_json(self):
        """Cadastro rapido via API JSON retorna o ID e nome do novo cliente."""
        response = self.client.post(
            "/clientes/rapido",
            json={"nome": "Cliente Expresso", "telefone": "11912345678", "empresa": "Express"},
        )
        self.assertEqual(response.status_code, 200)
        dados = response.get_json()
        self.assertEqual(dados["nome"], "Cliente Expresso")
        self.assertIn("id", dados)


if __name__ == "__main__":
    unittest.main()
