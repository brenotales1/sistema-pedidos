"""Testes automatizados para o modulo de autenticacao e perfis (US #1, CT01 e CT02)."""

import unittest
from app import create_app
from database.db import db
from models.usuario import Usuario


class AuthTestCase(unittest.TestCase):
    """Casos de teste para autenticacao, controle de sessao e perfis de acesso."""

    def setUp(self):
        """Configura ambiente de teste com banco em memoria."""
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            # Cria usuario Administrador se nao existir
            admin = Usuario.query.filter_by(email="admin@sistema.com").first()
            if not admin:
                admin = Usuario(
                    nome="Administrador Teste",
                    email="admin@sistema.com",
                    perfil="admin",
                )
                admin.definir_senha("123456")
                db.session.add(admin)

            # Cria usuario Funcionario se nao existir
            func = Usuario.query.filter_by(email="funcionario@sistema.com").first()
            if not func:
                func = Usuario(
                    nome="Funcionario Teste",
                    email="funcionario@sistema.com",
                    perfil="funcionario",
                )
                func.definir_senha("123456")
                db.session.add(func)

            db.session.commit()

    def tearDown(self):
        """Limpa banco ao final de cada teste."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_usuario_definir_e_verificar_senha(self):
        """Testa geracao de hash seguro e verificacao correta de senha."""
        with self.app.app_context():
            user = Usuario(nome="Unit Test", email="unit@teste.com", perfil="funcionario")
            user.definir_senha("minhasenha123")
            self.assertNotEqual(user.senha_hash, "minhasenha123")
            self.assertTrue(user.verificar_senha("minhasenha123"))
            self.assertFalse(user.verificar_senha("senhaerrada"))

    def test_ct01_login_credenciais_invalidas(self):
        """CT01: Login com credenciais invalidas deve ser recusado e exibir mensagem de erro."""
        response = self.client.post(
            "/login",
            data={"email": "admin@sistema.com", "senha": "senha_errada"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("E-mail ou senha".encode("utf-8"), response.data)

        # Testa com email inexistente
        response_inexistente = self.client.post(
            "/login",
            data={"email": "naoexiste@sistema.com", "senha": "123456"},
            follow_redirects=True,
        )
        self.assertEqual(response_inexistente.status_code, 200)
        self.assertIn("E-mail ou senha".encode("utf-8"), response_inexistente.data)

    def test_login_credenciais_validas(self):
        """Login com credenciais validas autentica o usuario e cria a sessao."""
        response = self.client.post(
            "/login",
            data={"email": "admin@sistema.com", "senha": "123456"},
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as sess:
            self.assertIn("usuario_id", sess)
            self.assertEqual(sess["usuario_nome"], "Administrador Teste")
            self.assertEqual(sess["usuario_perfil"], "admin")

    def test_ct02_acesso_restrito_perfil_funcionario(self):
        """CT02: Funcionario nao pode acessar rotas exclusivas de administrador."""
        # Autentica como funcionario
        self.client.post(
            "/login",
            data={"email": "funcionario@sistema.com", "senha": "123456"},
        )

        # Tenta acessar cadastro de material (exclusivo admin)
        response = self.client.get("/estoque/novo", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/")

        # Tenta criar categoria de material (exclusivo admin)
        response_post = self.client.post(
            "/estoque/categoria/nova",
            data={"nome": "Nova Categoria"},
            follow_redirects=False,
        )
        self.assertEqual(response_post.status_code, 302)
        self.assertEqual(response_post.location, "/")

    def test_acesso_permitido_perfil_admin(self):
        """Administrador tem acesso liberado para rotas restritas."""
        # Autentica como admin
        self.client.post(
            "/login",
            data={"email": "admin@sistema.com", "senha": "123456"},
        )

        response = self.client.get("/estoque/novo")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cadastrar Material".encode("utf-8"), response.data)

    def test_tela_estoque_oculta_acoes_administrativas_para_funcionario(self):
        """Funcionário não vê botões e formulários administrativos na tela de estoque."""
        self.client.post(
            "/login",
            data={"email": "funcionario@sistema.com", "senha": "123456"},
        )
        response = self.client.get("/estoque")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("+ Cadastrar Material".encode("utf-8"), response.data)
        self.assertNotIn("+ Tipo".encode("utf-8"), response.data)
        self.assertNotIn("<th>Ações</th>".encode("utf-8"), response.data)
        self.assertNotIn("+ Bobina".encode("utf-8"), response.data)
        # Mas consegue ver os dados do estoque e o leitor de código de barras
        self.assertIn("Identificar Material por Código de Barras".encode("utf-8"), response.data)
        self.assertIn("Lona Branca Brilho".encode("utf-8"), response.data)

    def test_tela_estoque_exibe_acoes_administrativas_para_admin(self):
        """Administrador visualiza todos os botões e opções de gestão no estoque."""
        self.client.post(
            "/login",
            data={"email": "admin@sistema.com", "senha": "123456"},
        )
        response = self.client.get("/estoque")
        self.assertEqual(response.status_code, 200)
        self.assertIn("+ Cadastrar Material".encode("utf-8"), response.data)
        self.assertIn("+ Tipo".encode("utf-8"), response.data)
        self.assertIn("<th>Ações</th>".encode("utf-8"), response.data)
        self.assertIn("+ Bobina".encode("utf-8"), response.data)

    def test_bloqueio_rotas_sem_login(self):
        """Acesso a rotas protegidas sem autenticacao redireciona para login."""
        rotas = ["/estoque", "/pedidos", "/clientes", "/estoque/novo"]
        for rota in rotas:
            response = self.client.get(rota, follow_redirects=False)
            self.assertEqual(response.status_code, 302, f"Rota {rota} deveria exigir login")
            self.assertIn("/login", response.location)

    def test_logout(self):
        """Logout limpa a sessao do usuario e redireciona para login."""
        self.client.post(
            "/login",
            data={"email": "admin@sistema.com", "senha": "123456"},
        )
        with self.client.session_transaction() as sess:
            self.assertIn("usuario_id", sess)

        response = self.client.get("/logout", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

        with self.client.session_transaction() as sess:
            self.assertNotIn("usuario_id", sess)


if __name__ == "__main__":
    unittest.main()
