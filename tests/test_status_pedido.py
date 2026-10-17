"""US #7: auditoria atomica em SQLite isolado, sem rede."""
import unittest
from unittest.mock import patch
from sqlalchemy import inspect, event
from tests import test_whatsapp as whatsapp_tests
from database.db import db
from models.pedido import Pedido
from models.historico_status_pedido import HistoricoStatusPedido
from services.pedido_service import atualizar_status_com_notificacao
from services.database_migration_service import garantir_tabela_historico_status_pedido


class StatusPedidoTestCase(unittest.TestCase):
    def setUp(self):
        # Reutiliza somente a fixture, sem duplicar os testes WhatsApp.
        self.fixture = whatsapp_tests.NotificacaoPedidoTestCase()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.app = self.fixture.app
        self.client = self.fixture.client
        self.pedido_id = self.fixture.pedido_id
        self.envio = patch('services.whatsapp_service.notificar_pedido_finalizado').start()
        self.addCleanup(patch.stopall)

    def alterar(self, status):
        return self.client.post(f'/pedidos/{self.pedido_id}/status',
                                data={'status': status}, follow_redirects=True)

    def test_historico_campos_repeticao_e_sequencia(self):
        self.alterar('Pronto para retirada')
        self.alterar('Pronto para retirada')
        self.alterar('Finalizado')
        with self.app.app_context():
            db.session.remove()
            linhas = HistoricoStatusPedido.query.order_by(HistoricoStatusPedido.id).all()
            self.assertEqual(len(linhas), 2)
            self.assertEqual((linhas[0].pedido_id, linhas[0].status_anterior,
                linhas[0].novo_status, linhas[0].usuario_id),
                (self.pedido_id, 'Pagamento pendente', 'Pronto para retirada', 1))
            self.assertIsNotNone(linhas[0].data_hora)
            self.assertEqual(linhas[1].status_anterior, 'Pronto para retirada')
            self.assertEqual(linhas[1].novo_status, 'Finalizado')
        self.envio.assert_called_once()

    def test_invalido_feedback_sem_alteracao(self):
        for valor in ('invalido', ''):
            resposta = self.alterar(valor)
            self.assertIn(b'Status do pedido invalido', resposta.data)
        self.verificar_sem_alteracao()

    def verificar_sem_alteracao(self):
        with self.app.app_context():
            self.assertEqual(db.session.get(Pedido, self.pedido_id).status, 'Pagamento pendente')
            self.assertEqual(HistoricoStatusPedido.query.count(), 0)
        self.envio.assert_not_called()

    def test_cliente_ausente_e_referencia_inexistente(self):
        for valor in (None, 999999):
            with self.app.app_context():
                db.session.get(Pedido, self.pedido_id).cliente_id = valor
                db.session.commit()
            self.assertIn(b'Vincule um cliente valido', self.alterar('Finalizado').data)
            self.verificar_sem_alteracao()

    def test_pedido_inexistente_e_sem_autenticacao(self):
        self.assertEqual(self.client.post('/pedidos/999999/status',
            data={'status': 'Finalizado'}).status_code, 404)
        with self.client.session_transaction() as sessao:
            sessao.clear()
        self.assertEqual(self.client.post(f'/pedidos/{self.pedido_id}/status',
            data={'status': 'Finalizado'}).status_code, 302)
        self.verificar_sem_alteracao()

    def test_usuario_inexistente(self):
        with self.client.session_transaction() as sessao:
            sessao['usuario_id'] = 999999
        self.assertIn(b'Usuario responsavel invalido', self.alterar('Finalizado').data)
        self.verificar_sem_alteracao()

    def test_falha_gravacao_historico_reverte_status(self):
        with self.app.app_context():
            pedido = db.session.get(Pedido, self.pedido_id)
            def falhar(*args):
                raise RuntimeError('falha auditoria')
            event.listen(HistoricoStatusPedido, 'before_insert', falhar)
            try:
                with self.assertRaises(RuntimeError):
                    atualizar_status_com_notificacao(pedido, 'Finalizado', usuario_id=1)
            finally:
                event.remove(HistoricoStatusPedido, 'before_insert', falhar)
        self.verificar_sem_alteracao()

    def test_migracao_idempotente_preserva_pedidos_e_historico(self):
        with self.app.app_context():
            HistoricoStatusPedido.__table__.drop(db.engine)
            garantir_tabela_historico_status_pedido()
            self.assertIn('historico_status_pedido', inspect(db.engine).get_table_names())
        self.alterar('Pronto para retirada')
        with self.app.app_context():
            garantir_tabela_historico_status_pedido()
            garantir_tabela_historico_status_pedido()
            self.assertEqual(Pedido.query.count(), 1)
            self.assertEqual(HistoricoStatusPedido.query.count(), 1)
