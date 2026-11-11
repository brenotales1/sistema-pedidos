"""Testes automatizados para inicializacao de estoque: preservacao de esgotados e parciais, larguras distintas e nao consolidacao automatica."""

import unittest
from unittest.mock import patch
from app import create_app, preparar_banco
from database.db import db
from models.bobina_estoque import BobinaEstoque
from models.material import Material
from services.material_service import seed_materials


class InicializacaoEstoqueTestCase(unittest.TestCase):
    """Cobre: reinicio nao repoe material esgotado nem altera saldo parcial; larguras diferentes separadas; consolidacao nao automatica."""

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_reiniciar_nao_repoe_material_esgotado(self):
        """Reiniciar aplicacao (ou rodar seed_materials) nao repoe bobinas de material esgotado."""
        mat = Material.query.filter_by(codigo_barras="7890000000011").first()
        self.assertIsNotNone(mat)

        # Esvazia completamente o material (0 bobinas, 0 metros)
        mat.bobinas.clear()
        db.session.commit()

        mat_esgotado = Material.query.filter_by(codigo_barras="7890000000011").first()
        self.assertEqual(mat_esgotado.quantidade_bobinas, 0)
        self.assertEqual(mat_esgotado.metros_disponiveis, 0.0)

        # Executa novamente a rotina de seed (simulando restart)
        seed_materials()

        mat_apos_reinicio = Material.query.filter_by(codigo_barras="7890000000011").first()
        self.assertEqual(
            mat_apos_reinicio.quantidade_bobinas, 0,
            "Material esgotado nao deve receber bobinas novas no reinicio",
        )
        self.assertEqual(
            mat_apos_reinicio.metros_disponiveis, 0.0,
            "Saldo zero deve permanecer inalterado",
        )

    def test_reiniciar_nao_altera_saldo_parcial(self):
        """Reiniciar aplicacao nao altera o saldo parcial de materiais existentes."""
        mat = Material.query.filter_by(codigo_barras="7890000000011").first()
        self.assertIsNotNone(mat)

        # Define metragem parcial (ex: 1 bobina com 17.85m)
        mat.bobinas.clear()
        mat.bobinas.append(BobinaEstoque(metros_restantes=17.85))
        db.session.commit()

        mat_parcial = Material.query.filter_by(codigo_barras="7890000000011").first()
        self.assertEqual(mat_parcial.metros_disponiveis, 17.85)

        # Roda seed_materials novamente
        seed_materials()

        mat_apos_seed = Material.query.filter_by(codigo_barras="7890000000011").first()
        self.assertEqual(mat_apos_seed.quantidade_bobinas, 1)
        self.assertEqual(
            mat_apos_seed.metros_disponiveis, 17.85,
            "Saldo parcial de 17.85m deve ser preservado sem alteracao",
        )

    def test_materiais_com_larguras_diferentes_continuam_separados(self):
        """Materiais com mesma categoria e nome, porem com larguras distintas, permanecem separados."""
        # Cadastra variacao de mesma categoria e nome com largura diferente
        mat_120 = Material(
            categoria="Adesivo",
            nome="Adesivo Fosco Premium",
            largura_m=1.20,
            codigo_barras="7898887771200",
        )
        mat_150 = Material(
            categoria="Adesivo",
            nome="Adesivo Fosco Premium",
            largura_m=1.50,
            codigo_barras="7898887771500",
        )
        mat_120.bobinas.append(BobinaEstoque(metros_restantes=50.0))
        mat_150.bobinas.append(BobinaEstoque(metros_restantes=50.0))
        db.session.add_all([mat_120, mat_150])
        db.session.commit()

        # Executa rotina de seed
        seed_materials()

        # Confere que continuam existindo como dois materiais distintos
        itens = Material.query.filter_by(nome="Adesivo Fosco Premium").all()
        self.assertEqual(len(itens), 2)
        larguras = sorted([item.largura_m for item in itens])
        self.assertEqual(larguras, [1.20, 1.50])

    def test_consolidacao_nao_executa_automaticamente(self):
        """A consolidacao de materiais repetidos nao e executada automaticamente na inicializacao."""
        with patch("services.material_service.consolidar_materiais_repetidos") as mock_consolidar:
            preparar_banco()
            mock_consolidar.assert_not_called()


if __name__ == "__main__":
    unittest.main()
