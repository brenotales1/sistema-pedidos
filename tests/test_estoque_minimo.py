"""Testes automatizados para US #11 — Estoque minimo: cadastro, edicao, permissoes, alertas, filtros e migracao."""

import unittest
from app import create_app
from database.db import db
from models.material import Material
from models.usuario import Usuario
from services.constantes import METROS_POR_BOBINA
from services.database_migration_service import garantir_coluna_estoque_minimo_material
from services.estoque_service import adicionar_bobina, ajustar_metros_disponiveis


class EstoqueMinimoTestCase(unittest.TestCase):
    """Cobre US #11: cadastro e edicao por admin, bloqueio para funcionario, validacoes, alerta < minimo, filtros e migracao."""

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            self.admin = Usuario(nome="Admin Estoque", email="admin.est@sistema.com", perfil="admin")
            self.admin.definir_senha("123456")
            self.func = Usuario(nome="Funcionario Estoque", email="func.est@sistema.com", perfil="funcionario")
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
            sess["usuario_nome"] = "Admin Estoque"

    def logar_funcionario(self):
        with self.client.session_transaction() as sess:
            sess["usuario_id"] = self.func_id
            sess["usuario_perfil"] = "funcionario"
            sess["usuario_nome"] = "Funcionario Estoque"

    def test_cadastro_material_com_estoque_minimo_admin(self):
        """Administrador cadastra material com limite de estoque minimo configurado."""
        self.logar_admin()
        response = self.client.post(
            "/estoque/novo",
            data={
                "categoria": "Adesivo",
                "nome": "Vinil Eletrostatico",
                "codigo_barras": "7891230009999",
                "largura_m": "1.00",
                "unidades": "1",
                "estoque_minimo": "25.50",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            mat = Material.query.filter_by(codigo_barras="7891230009999").first()
            self.assertIsNotNone(mat)
            self.assertEqual(mat.estoque_minimo, 25.50)
            self.assertEqual(mat.estoque_minimo_formatado, "25,50m")

    def test_edicao_estoque_minimo_admin(self):
        """Administrador edita o estoque minimo de um material existente com sucesso."""
        self.logar_admin()
        response = self.client.post(
            f"/estoque/material/{self.material_id}/estoque-minimo",
            data={"estoque_minimo": "45.0"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Estoque minimo atualizado com sucesso".encode("utf-8"), response.data)

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.estoque_minimo, 45.00)

    def test_bloqueio_edicao_estoque_minimo_para_funcionario(self):
        """Funcionario e bloqueado ao tentar alterar o estoque minimo."""
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            minimo_original = mat.estoque_minimo

        self.logar_funcionario()
        response = self.client.post(
            f"/estoque/material/{self.material_id}/estoque-minimo",
            data={"estoque_minimo": "99.0"},
            follow_redirects=False,
        )
        # Redireciona para home devido a bloqueio do admin_required
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/")

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.estoque_minimo, minimo_original, "Estoque minimo nao deve ser alterado por funcionario")

    def test_rejeicao_valores_invalidos_estoque_minimo(self):
        """Rejeita valores negativos, nao numericos ou invalidos de estoque minimo."""
        self.logar_admin()
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            mat.estoque_minimo = 10.00
            db.session.commit()

        valores_invalidos = ["-5.0", "-0.01", "texto_invalido", "", "inf", "nan"]

        for valor in valores_invalidos:
            with self.subTest(valor=valor):
                response = self.client.post(
                    f"/estoque/material/{self.material_id}/estoque-minimo",
                    data={"estoque_minimo": valor},
                    follow_redirects=True,
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn("Informe um estoque minimo finito".encode("utf-8"), response.data)

                with self.app.app_context():
                    mat = db.session.get(Material, self.material_id)
                    self.assertEqual(mat.estoque_minimo, 10.00, "Valor invalido nao deve sobrescrever o limite anterior")

    def test_alerta_somente_quando_saldo_menor_que_minimo(self):
        """Alerta de estoque baixo e ativado estritamente quando saldo < minimo, nao quando igual ou superior."""
        self.logar_admin()
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            mat.estoque_minimo = 50.00
            # Define metragem exatamente igual ao minimo (50.00m)
            ajustar_metros_disponiveis(mat, 50.00)
            db.session.commit()

            # Saldo == Minimo -> NAO esta abaixo do minimo!
            self.assertEqual(mat.metros_disponiveis, 50.00)
            self.assertFalse(mat.abaixo_estoque_minimo)

        # Na interface com saldo == minimo:
        resp_igual = self.client.get("/estoque")
        self.assertEqual(resp_igual.status_code, 200)
        conteudo_igual = resp_igual.data.decode("utf-8")
        self.assertIn("Dentro do limite", conteudo_igual)

        # Agora define metragem estritamente abaixo do minimo (49.99m)
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            ajustar_metros_disponiveis(mat, 49.99)
            db.session.commit()

            # Saldo < Minimo -> ESTA abaixo do minimo!
            self.assertTrue(mat.abaixo_estoque_minimo)

        resp_menor = self.client.get("/estoque")
        self.assertEqual(resp_menor.status_code, 200)
        conteudo_menor = resp_menor.data.decode("utf-8")
        self.assertIn("Abaixo do mínimo — repor", conteudo_menor)
        self.assertIn("estoque-abaixo-minimo", conteudo_menor)

        # Saldo > Minimo (ex: 80.00m)
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            ajustar_metros_disponiveis(mat, 80.00)
            db.session.commit()
            self.assertFalse(mat.abaixo_estoque_minimo)

    def test_filtro_abaixo_minimo_na_tela_estoque(self):
        """Filtro ?abaixo_minimo=1 exibe apenas materiais com saldo inferior ao minimo."""
        self.logar_admin()
        with self.app.app_context():
            # Material 1: Abaixo do minimo
            mat1 = db.session.get(Material, self.material_id)
            mat1.estoque_minimo = 80.00
            ajustar_metros_disponiveis(mat1, 40.00)  # 40 < 80 -> Abaixo

            # Material 2: Acima do minimo
            mat2 = Material.query.filter_by(codigo_barras="7890000000028").first()
            if mat2:
                mat2.estoque_minimo = 10.00
                ajustar_metros_disponiveis(mat2, 50.00)  # 50 > 10 -> Dentro

            db.session.commit()

        response = self.client.get("/estoque?abaixo_minimo=1")
        self.assertEqual(response.status_code, 200)
        conteudo = response.data.decode("utf-8")

        # Material 1 deve aparecer
        self.assertIn("Lona Branca Brilho", conteudo)
        self.assertIn("Abaixo do mínimo — repor", conteudo)

        # Material 2 nao deve aparecer nos itens filtrados
        self.assertNotIn("Adesivo Branco Brilho", conteudo)

    def test_persistencia_estoque_minimo(self):
        """Valor do estoque minimo e persistido corretamente no banco de dados."""
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            mat.estoque_minimo = 12.34
            db.session.commit()

        # Recarrega em uma nova sessao
        with self.app.app_context():
            mat_recarregado = db.session.get(Material, self.material_id)
            self.assertEqual(mat_recarregado.estoque_minimo, 12.34)

    def test_migracao_estoque_minimo_preservando_dados(self):
        """Rotina de migracao garante a coluna sem alterar saldos ou limites ja cadastrados."""
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            mat.estoque_minimo = 22.00
            saldo_antes = mat.metros_disponiveis
            db.session.commit()

            # Executa a rotina de migracao
            garantir_coluna_estoque_minimo_material()
            db.session.commit()

            mat_depois = db.session.get(Material, self.material_id)
            self.assertEqual(mat_depois.estoque_minimo, 22.00, "Limite preexistente deve ser preservado")
            self.assertEqual(mat_depois.metros_disponiveis, saldo_antes, "Saldo em estoque nao deve ser alterado")


if __name__ == "__main__":
    unittest.main()
