"""CT45: auditoria e uma tentativa por transicao de finalizacao."""
import unittest
import requests
from notificacao_base import NotificacaoMixin
from database.db import db
from models.pedido import Pedido
from models.historico_status_pedido import HistoricoStatusPedido
from models.notificacao_whatsapp import NotificacaoWhatsApp


class NotificacaoPersistenciaTestCase(NotificacaoMixin, unittest.TestCase):
    def test_ct45_auditoria_destinatario_e_aceite_sem_entrega(self):
        self.envio_simulado_habilitado()
        self.finalizar()
        with self.app.app_context():
            db.session.remove()
            tentativa = NotificacaoWhatsApp.query.one()
            historico = HistoricoStatusPedido.query.one()
            self.assertEqual(tentativa.pedido_id, self.pedido_id)
            self.assertEqual(tentativa.cliente_id, self.cliente_id)
            self.assertEqual(tentativa.historico_status_id, historico.id)
            self.assertEqual(historico.usuario_id, self.usuario_id)
            self.assertEqual(historico.status_anterior, "Pronto para retirada")
            self.assertEqual(historico.novo_status, "Finalizado")
            self.assertEqual(tentativa.evento, "pedido_finalizado")
            self.assertIsNotNone(tentativa.data_hora)
            self.assertEqual(tentativa.resultado, "aceito")
            self.assertEqual(tentativa.message_sid, "wamidTESTE123")
            self.assertFalse(tentativa.entrega_confirmada)
        self.assertEqual(self.post.call_args.kwargs["json"]["to"], "5511999999999")

    def test_ct43_falhas_http_persistidas_sem_desfazer_finalizacao(self):
        self.envio_simulado_habilitado()
        for codigo in (400, 500):
            with self.subTest(codigo=codigo):
                self.post.return_value.status_code = codigo
                self.finalizar()
                with self.app.app_context():
                    db.session.remove()
                    tentativa = NotificacaoWhatsApp.query.order_by(NotificacaoWhatsApp.id.desc()).first()
                    self.assertEqual(tentativa.resultado, "falha")
                    self.assertEqual(tentativa.codigo_erro, codigo)
                    self.assertIsNone(tentativa.message_sid)
                    self.assertFalse(tentativa.entrega_confirmada)
                    self.assertEqual(db.session.get(Pedido, self.pedido_id).status, "Finalizado")
                self.finalizar("Pronto para retirada")

    def test_ct43_erro_rede_persistido(self):
        self.envio_simulado_habilitado()
        self.post.side_effect = requests.ConnectionError("simulado")
        self.finalizar()
        with self.app.app_context():
            db.session.remove()
            tentativa = NotificacaoWhatsApp.query.one()
            self.assertEqual(tentativa.resultado, "falha")
            self.assertIsNone(tentativa.codigo_erro)
            self.assertIsNone(tentativa.message_sid)
            self.assertEqual(db.session.get(Pedido, self.pedido_id).status, "Finalizado")

    def test_ct45_repetir_status_nao_duplica_nem_reenvia(self):
        self.envio_simulado_habilitado()
        self.finalizar()
        self.finalizar()
        self.post.assert_called_once()
        with self.app.app_context():
            self.assertEqual(NotificacaoWhatsApp.query.count(), 1)
            self.assertEqual(HistoricoStatusPedido.query.count(), 1)

    def test_ct45_outro_status_nao_dispara_e_nova_finalizacao_cria_tentativa(self):
        self.envio_simulado_habilitado()
        self.finalizar("Pagamento pendente")
        self.post.assert_not_called()
        with self.app.app_context():
            self.assertEqual(NotificacaoWhatsApp.query.count(), 0)
        self.finalizar()
        self.finalizar("Pronto para retirada")
        self.finalizar()
        self.assertEqual(self.post.call_count, 2)
        with self.app.app_context():
            tentativas = NotificacaoWhatsApp.query.all()
            self.assertEqual(len(tentativas), 2)
            self.assertNotEqual(tentativas[0].historico_status_id, tentativas[1].historico_status_id)

    def test_testing_persiste_bloqueio_e_finaliza_sem_rede(self):
        self.finalizar()
        with self.app.app_context():
            tentativa = NotificacaoWhatsApp.query.one()
            self.assertEqual(tentativa.resultado, "bloqueado_testing")
            self.assertFalse(tentativa.entrega_confirmada)
        self.post.assert_not_called()
        self.rede.assert_not_called()
