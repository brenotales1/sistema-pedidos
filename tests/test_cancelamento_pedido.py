"""Testes automatizados para regras de cancelamento de pedidos: permissao, bloqueios e preservacao de estoque."""

import unittest
from app import create_app
from database.db import db
from models.cliente import Cliente
from models.material import Material
from models.movimentacao_estoque import MovimentacaoEstoque
from models.pedido import Pedido
from models.usuario import Usuario
from services.estoque_service import adicionar_bobina


class CancelamentoPedidoTestCase(unittest.TestCase):
    """Cobre: permitir em Pagamento pendente e Aguardando producao; bloquear em Pronto para retirada e Finalizado."""

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            self.operador = Usuario(nome="Operador Pedidos", email="operador@sistema.com", perfil="funcionario")
            self.operador.definir_senha("123456")
            db.session.add(self.operador)

            self.cliente = Cliente(nome="Cliente Cancelamento", telefone="11977776666")
            db.session.add(self.cliente)
            db.session.commit()

            self.operador_id = self.operador.id
            self.cliente_id = self.cliente.id

            self.mat = Material.query.filter_by(codigo_barras="7890000000011").first()
            if self.mat and len(self.mat.bobinas) < 2:
                adicionar_bobina(self.mat, 2 - len(self.mat.bobinas))
                db.session.commit()
            self.material_id = self.mat.id

        self.logar_operador()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def logar_operador(self):
        with self.client.session_transaction() as sess:
            sess["usuario_id"] = self.operador_id
            sess["usuario_perfil"] = "funcionario"
            sess["usuario_nome"] = "Operador Pedidos"

    def criar_pedido_teste(self, status="Pagamento pendente"):
        """Cria um pedido consumindo 2.00m de Lona Branca Brilho."""
        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            pedido = Pedido(
                cliente_id=self.cliente_id,
                cliente_nome="Cliente Cancelamento",
                categoria="Lona",
                material_nome="Lona Branca Brilho",
                largura_pedido_m=1.0,
                altura_pedido_m=2.0,
                quantidade=1,
                unidade_medida="m",
                largura_bobina_usada_m=3.20,
                orientacao="Rotacionado",
                metros_consumidos=1.0,
                area_total_m2=2.0,
                status=status,
            )
            # Baixa 1.0m do material
            mat.bobinas[0].metros_restantes = round(mat.bobinas[0].metros_restantes - 1.0, 2)
            db.session.add(pedido)
            db.session.commit()
            return pedido.id

    def test_cancelamento_permitido_em_pagamento_pendente(self):
        """Permite cancelamento quando status for 'Pagamento pendente', devolvendo material e registrando estorno."""
        pedido_id = self.criar_pedido_teste(status="Pagamento pendente")

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            saldo_antes = mat.metros_disponiveis

        response = self.client.post(f"/pedidos/{pedido_id}/cancelar", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            self.assertIsNone(db.session.get(Pedido, pedido_id), "Pedido deve ser excluido ao cancelar")

            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.metros_disponiveis, round(saldo_antes + 1.0, 2), "Metragem deve retornar ao estoque")

            mov = MovimentacaoEstoque.query.filter_by(
                material_id=self.material_id, tipo="entrada"
            ).order_by(MovimentacaoEstoque.id.desc()).first()
            self.assertIsNotNone(mov)
            self.assertEqual(mov.motivo, f"Estorno por cancelamento do pedido #{pedido_id}")
            self.assertEqual(mov.quantidade_metros, 1.0)

    def test_cancelamento_permitido_em_aguardando_producao(self):
        """Permite cancelamento quando status for 'Aguardando produção', devolvendo estoque."""
        pedido_id = self.criar_pedido_teste(status="Aguardando produção")

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            saldo_antes = mat.metros_disponiveis

        response = self.client.post(f"/pedidos/{pedido_id}/cancelar", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            self.assertIsNone(db.session.get(Pedido, pedido_id), "Pedido deve ser excluido")

            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.metros_disponiveis, round(saldo_antes + 1.0, 2))

            mov = MovimentacaoEstoque.query.filter_by(
                material_id=self.material_id, tipo="entrada"
            ).order_by(MovimentacaoEstoque.id.desc()).first()
            self.assertIsNotNone(mov)
            self.assertEqual(mov.motivo, f"Estorno por cancelamento do pedido #{pedido_id}")

    def test_bloquear_cancelamento_em_pronto_para_retirada_requisicao_direta(self):
        """Bloqueia cancelamento em 'Pronto para retirada' mesmo por POST direto, preservando pedido e saldo."""
        pedido_id = self.criar_pedido_teste(status="Pronto para retirada")

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            saldo_antes = mat.metros_disponiveis
            total_mov_antes = MovimentacaoEstoque.query.count()

        # Envia POST direto para cancelar
        response = self.client.post(f"/pedidos/{pedido_id}/cancelar", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Pedidos prontos ou finalizados não podem ser cancelados".encode("utf-8"),
            response.data,
        )

        with self.app.app_context():
            pedido = db.session.get(Pedido, pedido_id)
            self.assertIsNotNone(pedido, "Pedido deve ser preservado")
            self.assertEqual(pedido.status, "Pronto para retirada")

            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.metros_disponiveis, saldo_antes, "Saldo deve ser estritamente preservado")
            self.assertEqual(MovimentacaoEstoque.query.count(), total_mov_antes, "Nao deve registrar movimentacao")

    def test_bloquear_cancelamento_em_finalizado_requisicao_direta(self):
        """Bloqueia cancelamento em 'Finalizado' mesmo por POST direto, preservando pedido e saldo."""
        pedido_id = self.criar_pedido_teste(status="Finalizado")

        with self.app.app_context():
            mat = db.session.get(Material, self.material_id)
            saldo_antes = mat.metros_disponiveis
            total_mov_antes = MovimentacaoEstoque.query.count()

        response = self.client.post(f"/pedidos/{pedido_id}/cancelar", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Pedidos prontos ou finalizados não podem ser cancelados".encode("utf-8"),
            response.data,
        )

        with self.app.app_context():
            pedido = db.session.get(Pedido, pedido_id)
            self.assertIsNotNone(pedido, "Pedido finalizado deve ser preservado")
            self.assertEqual(pedido.status, "Finalizado")

            mat = db.session.get(Material, self.material_id)
            self.assertEqual(mat.metros_disponiveis, saldo_antes, "Saldo de estoque nao pode retornar")
            self.assertEqual(MovimentacaoEstoque.query.count(), total_mov_antes, "Nao deve registrar movimentacao")

    def test_interface_oculta_botao_cancelamento_para_pronto_e_finalizado(self):
        """Botao de cancelamento e exibido apenas para 'Pagamento pendente' e 'Aguardando producao', sendo oculto nos demais."""
        # 1. Pagamento pendente -> exibe botao
        p_pendente = self.criar_pedido_teste(status="Pagamento pendente")
        resp_pendente = self.client.get(f"/pedidos/{p_pendente}/editar")
        self.assertEqual(resp_pendente.status_code, 200)
        self.assertIn("Apagar/Cancelar Pedido".encode("utf-8"), resp_pendente.data)

        # 2. Aguardando producao -> exibe botao
        p_aguardando = self.criar_pedido_teste(status="Aguardando produção")
        resp_aguardando = self.client.get(f"/pedidos/{p_aguardando}/editar")
        self.assertEqual(resp_aguardando.status_code, 200)
        self.assertIn("Apagar/Cancelar Pedido".encode("utf-8"), resp_aguardando.data)

        # 3. Pronto para retirada -> oculto
        p_pronto = self.criar_pedido_teste(status="Pronto para retirada")
        resp_pronto = self.client.get(f"/pedidos/{p_pronto}/editar")
        self.assertEqual(resp_pronto.status_code, 200)
        self.assertNotIn("Apagar/Cancelar Pedido".encode("utf-8"), resp_pronto.data)

        # 4. Finalizado -> oculto
        p_finalizado = self.criar_pedido_teste(status="Finalizado")
        resp_finalizado = self.client.get(f"/pedidos/{p_finalizado}/editar")
        self.assertEqual(resp_finalizado.status_code, 200)
        self.assertNotIn("Apagar/Cancelar Pedido".encode("utf-8"), resp_finalizado.data)


if __name__ == "__main__":
    unittest.main()
