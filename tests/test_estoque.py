"""Testes automatizados para o modulo de estoque e materiais (US #2, US #3, CT03, CT04 e CT05)."""

import unittest
from app import create_app
from database.db import db
from models.bobina_estoque import BobinaEstoque
from models.categoria_material import CategoriaMaterial
from models.material import Material
from models.usuario import Usuario
from services.constantes import METROS_POR_BOBINA
from services.estoque_service import (
    adicionar_bobina,
    ajustar_metros_disponiveis,
    consumir_material,
    devolver_material,
    remover_bobina,
)


class EstoqueTestCase(unittest.TestCase):
    """Casos de teste para controle de materiais, bobinas e busca no estoque."""

    def setUp(self):
        """Configura ambiente de teste isolado com banco em memoria."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            # Cria usuario administrador se nao existir
            admin = Usuario.query.filter_by(email="admin@sistema.com").first()
            if not admin:
                admin = Usuario(nome="Admin Teste", email="admin@sistema.com", perfil="admin")
                admin.definir_senha("123456")
                db.session.add(admin)

            # Localiza material base semeado e garante 2 bobinas para o teste
            mat = Material.query.filter_by(codigo_barras="7890000000011").first()
            if mat:
                if len(mat.bobinas) < 2:
                    adicionar_bobina(mat, 2 - len(mat.bobinas))
            db.session.commit()

        # Realiza login como administrador para os testes de rota
        self.client.post("/login", data={"email": "admin@sistema.com", "senha": "123456"})

    def tearDown(self):
        """Limpa banco ao final de cada teste."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_ct03_cadastro_material_codigo_barras_duplicado(self):
        """CT03: Cadastro de material com codigo de barras duplicado deve ser recusado."""
        response = self.client.post(
            "/estoque/novo",
            data={
                "categoria": "Lona",
                "nome": "Lona Fosca Nova",
                "codigo_barras": "7890000000011",  # Codigo ja existente
                "largura_m": "3.20",
                "unidades": "1",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Esse código de barras já está cadastrado".encode("utf-8"), response.data)

        # Garante que nao inseriu no banco
        with self.app.app_context():
            materiais = Material.query.filter_by(codigo_barras="7890000000011").all()
            self.assertEqual(len(materiais), 1)
            self.assertEqual(materiais[0].nome, "Lona Branca Brilho")

    def test_cadastro_material_com_sucesso(self):
        """Cadastro de material com dados validos e codigo de barras unico e persistido."""
        response = self.client.post(
            "/estoque/novo",
            data={
                "categoria": "Adesivo",
                "nome": "Vinil Perfurado",
                "codigo_barras": "7890000099999",
                "largura_m": "1.37",
                "unidades": "3",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Material cadastrado com sucesso".encode("utf-8"), response.data)

        with self.app.app_context():
            mat = Material.query.filter_by(codigo_barras="7890000099999").first()
            self.assertIsNotNone(mat)
            self.assertEqual(mat.nome, "Vinil Perfurado")
            self.assertEqual(mat.quantidade_bobinas, 3)
            self.assertEqual(mat.metros_disponiveis, 150.0)

    def test_validacao_campos_invalidos_cadastro_material(self):
        """Recusa cadastro quando largura ou unidades sao menores ou iguais a zero."""
        response = self.client.post(
            "/estoque/novo",
            data={
                "categoria": "Adesivo",
                "nome": "Adesivo Invalido",
                "codigo_barras": "7899999999999",
                "largura_m": "0",
                "unidades": "-1",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Preencha tipo, nome, código de barras".encode("utf-8"), response.data)

    def test_ct04_consulta_material_inexistente(self):
        """CT04: Busca por material inexistente nao quebra e retorna tela sem resultados."""
        response = self.client.get("/estoque?busca=CODIGO_QUE_NAO_EXISTE_999")
        self.assertEqual(response.status_code, 200)
        # Nao deve exibir o material cadastrado nos resultados filtrados
        self.assertNotIn("7890000000011".encode("utf-8"), response.data)

    def test_consulta_material_por_codigo_barras_existente(self):
        """Busca por codigo de barras existente localiza o material com sucesso."""
        response = self.client.get("/estoque?busca=7890000000011")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Lona Branca Brilho".encode("utf-8"), response.data)
        self.assertIn("7890000000011".encode("utf-8"), response.data)

    def test_regras_servico_bobinas(self):
        """Testa adicao, remocao e ajuste de metragem no estoque_service."""
        with self.app.app_context():
            mat = Material.query.filter_by(codigo_barras="7890000000011").first()
            self.assertEqual(mat.quantidade_bobinas, 2)
            self.assertEqual(mat.metros_disponiveis, 100.0)

            # Adicionar bobina
            adicionar_bobina(mat, 1)
            self.assertEqual(mat.quantidade_bobinas, 3)
            self.assertEqual(mat.metros_disponiveis, 150.0)

            # Remover bobina
            removido = remover_bobina(mat)
            self.assertTrue(removido)
            self.assertEqual(mat.quantidade_bobinas, 2)

            # Ajustar metros
            ajustar_metros_disponiveis(mat, 75.50)
            self.assertEqual(mat.metros_disponiveis, 75.50)

    def test_consumo_e_devolucao_material(self):
        """Testa baixa automatizada e devolucao de estoque de material."""
        with self.app.app_context():
            mat = Material.query.filter_by(codigo_barras="7890000000011").first()
            # Consome 30 metros de 100 disponiveis
            sucesso = consumir_material(mat, 30.0)
            self.assertTrue(sucesso)
            self.assertEqual(mat.metros_disponiveis, 70.0)

            # Tenta consumir mais do que disponivel
            falha = consumir_material(mat, 100.0)
            self.assertFalse(falha)
            self.assertEqual(mat.metros_disponiveis, 70.0)

            # Devolve 30 metros
            devolver_material(mat, 30.0)
            self.assertEqual(mat.metros_disponiveis, 100.0)


if __name__ == "__main__":
    unittest.main()
