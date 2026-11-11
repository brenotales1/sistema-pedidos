"""Testes automatizados para regularizacao e edicao de codigos de barras de materiais antigos."""

import unittest
from app import create_app
from database.db import db
from models.material import Material
from models.movimentacao_estoque import MovimentacaoEstoque
from models.usuario import Usuario
from services.estoque_service import adicionar_bobina, registrar_movimentacao


class CodigoBarrasMateriaisTestCase(unittest.TestCase):
    """Cobre: admin cadastra e corrige codigo, bloqueio para funcionario, rejeicao de vazio/invalido/duplicado, preservacao de estoque e historico, consulta e entrada com codigo salvo."""

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            self.admin = Usuario(nome="Admin Barcode", email="admin.bar@sistema.com", perfil="admin")
            self.admin.definir_senha("123456")
            self.func = Usuario(nome="Funcionario Barcode", email="func.bar@sistema.com", perfil="funcionario")
            self.func.definir_senha("123456")
            db.session.add_all([self.admin, self.func])
            db.session.commit()

            self.admin_id = self.admin.id
            self.func_id = self.func.id

            mat = Material.query.filter_by(codigo_barras="7890000000011").first()
            if mat and len(mat.bobinas) < 2:
                adicionar_bobina(mat, 2 - len(mat.bobinas))
                db.session.commit()
            self.material_id = mat.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def logar_admin(self):
        with self.client.session_transaction() as sess:
            sess["usuario_id"] = self.admin_id
            sess["usuario_perfil"] = "admin"
            sess["usuario_nome"] = "Admin Barcode"

    def logar_funcionario(self):
        with self.client.session_transaction() as sess:
            sess["usuario_id"] = self.func_id
            sess["usuario_perfil"] = "funcionario"
            sess["usuario_nome"] = "Funcionario Barcode"

    def test_admin_cadastra_e_corrige_codigo_barras(self):
        """Administrador cadastra e corrige o codigo de barras com sucesso."""
        self.logar_admin()
        novo_codigo = "7899990001112"

        response = self.client.post(
            f"/estoque/material/{self.material_id}/codigo-barras",
            data={"codigo_barras": novo_codigo},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Código de barras atualizado com sucesso".encode("utf-8"), response.data)

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.codigo_barras, novo_codigo)

    def test_funcionario_nao_pode_alterar_codigo_barras(self):
        """Funcionario nao tem permissao para alterar o codigo de barras de material."""
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            codigo_original = mat.codigo_barras

        self.logar_funcionario()
        response = self.client.post(
            f"/estoque/material/{self.material_id}/codigo-barras",
            data={"codigo_barras": "7890000099999"},
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/")

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.codigo_barras, codigo_original, "Codigo nao deve ser alterado por funcionario")

    def test_rejeitar_codigo_barras_vazio(self):
        """Rejeita tentativa de salvar codigo de barras vazio ou contendo apenas espacos."""
        self.logar_admin()
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            codigo_original = mat.codigo_barras

        for vazio in ["", "   ", "\t"]:
            with self.subTest(vazio=vazio):
                response = self.client.post(
                    f"/estoque/material/{self.material_id}/codigo-barras",
                    data={"codigo_barras": vazio},
                    follow_redirects=True,
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn("Informe um código de barras válido".encode("utf-8"), response.data)

                with self.app.app_context():
                    mat = db.session.get(Material, self.material_id)
                    self.assertEqual(mat.codigo_barras, codigo_original)

    def test_rejeitar_codigo_barras_invalido(self):
        """Rejeita codigos com mais de 50 caracteres ou caracteres de controle nao imprimiveis."""
        self.logar_admin()
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            codigo_original = mat.codigo_barras

        longo = "1" * 51
        com_controle = "789000\x00123"

        for invalido in [longo, com_controle]:
            with self.subTest(invalido=invalido):
                response = self.client.post(
                    f"/estoque/material/{self.material_id}/codigo-barras",
                    data={"codigo_barras": invalido},
                    follow_redirects=True,
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn("Informe um código de barras válido".encode("utf-8"), response.data)

                with self.app.app_context():
                    mat = db.session.get(Material, self.material_id)
                    self.assertEqual(mat.codigo_barras, codigo_original)

    def test_rejeitar_codigo_barras_duplicado(self):
        """Rejeita alteracao para codigo de barras que ja pertence a outro material."""
        self.logar_admin()
        with self.app.app_context():
            outro_material = Material.query.filter_by(codigo_barras="7890000000028").first()
            codigo_duplicado = outro_material.codigo_barras

            mat = db.session.get(Material, self.material_id)
            codigo_original = mat.codigo_barras

        response = self.client.post(
            f"/estoque/material/{self.material_id}/codigo-barras",
            data={"codigo_barras": codigo_duplicado},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("já está cadastrado em outro material".encode("utf-8"), response.data)

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.codigo_barras, codigo_original)

    def test_preservar_estoque_e_historico_ao_alterar_codigo(self):
        """Alterar o codigo de barras preserva integralmente as bobinas, o saldo e o historico de movimentacoes."""
        self.logar_admin()
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            registrar_movimentacao(mat, "entrada", 50.0, self.admin_id, "Movimentacao antiga vinculada")
            db.session.commit()

            bobinas_antes = mat.quantidade_bobinas
            metros_antes = mat.metros_disponiveis
            total_mov_antes = MovimentacaoEstoque.query.filter_by(material_id=self.material_id).count()

        # Atualiza o codigo de barras
        response = self.client.post(
            f"/estoque/material/{self.material_id}/codigo-barras",
            data={"codigo_barras": "7891112223334"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.codigo_barras, "7891112223334")
            self.assertEqual(mat.quantidade_bobinas, bobinas_antes, "Bobinas devem ser preservadas")
            self.assertEqual(mat.metros_disponiveis, metros_antes, "Metragem total deve ser preservada")

            total_mov_depois = MovimentacaoEstoque.query.filter_by(material_id=self.material_id).count()
            self.assertEqual(total_mov_antes, total_mov_depois, "Historico de movimentacoes deve ser preservado")

    def test_confirmar_consulta_e_entrada_usando_codigo_salvo(self):
        """Material com codigo atualizado e localizado na busca, na API e permite entrada via codigo de barras."""
        self.logar_admin()
        novo_codigo = "7897776665554"

        # 1. Atualiza o codigo
        self.client.post(
            f"/estoque/material/{self.material_id}/codigo-barras",
            data={"codigo_barras": novo_codigo},
            follow_redirects=True,
        )

        # 2. Confirma busca na listagem de estoque
        resp_busca = self.client.get(f"/estoque?busca={novo_codigo}")
        self.assertEqual(resp_busca.status_code, 200)
        self.assertIn("Lona Branca Brilho".encode("utf-8"), resp_busca.data)
        self.assertIn(novo_codigo.encode("utf-8"), resp_busca.data)

        # 3. Confirma consulta na API JSON de identificacao
        resp_api = self.client.get(f"/estoque/api/material/codigo/{novo_codigo}")
        self.assertEqual(resp_api.status_code, 200)
        dados = resp_api.get_json()
        self.assertEqual(dados["codigo_barras"], novo_codigo)
        self.assertEqual(dados["nome"], "Lona Branca Brilho")

        # 4. Confirma registro de entrada de estoque usando o novo codigo
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            bobinas_antes = mat.quantidade_bobinas

        resp_entrada = self.client.post(
            "/estoque/entrada",
            data={
                "codigo_barras": novo_codigo,
                "quantidade_bobinas": "2",
                "motivo": "Entrada teste apos correcao de codigo",
            },
            follow_redirects=True,
        )
        self.assertEqual(resp_entrada.status_code, 200)
        self.assertIn("Entrada de 2 bobina(s) registrada com sucesso".encode("utf-8"), resp_entrada.data)

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.quantidade_bobinas, bobinas_antes + 2)

            mov = MovimentacaoEstoque.query.filter_by(
                material_id=self.material_id, tipo="entrada"
            ).order_by(MovimentacaoEstoque.id.desc()).first()
            self.assertIsNotNone(mov)
            self.assertEqual(mov.motivo, "Entrada teste apos correcao de codigo")
            self.assertEqual(mov.quantidade_bobinas, 2)


if __name__ == "__main__":
    unittest.main()
