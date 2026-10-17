"""CT42 / US #8 (CT08 de notificacoes na retrospectiva): feedback visual."""
import unittest
from unittest.mock import patch
from tests import test_whatsapp as whatsapp_tests
from database.db import db
from models.pedido import Pedido
from models.historico_status_pedido import HistoricoStatusPedido
import requests
import os


class NotificacaoVisualTestCase(unittest.TestCase):
    def setUp(self):
        self.fixture = whatsapp_tests.NotificacaoPedidoTestCase()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.app = self.fixture.app
        self.client = self.fixture.client
        self.pedido_id = self.fixture.pedido_id
        # Exercita o servico real; transporte e SDK continuam bloqueados/simulados.
        self.app.config.update(TESTING=False)
        guard = patch('services.whatsapp_service.requests.post')
        self.sdk = guard.start()
        self.addCleanup(guard.stop)
        self.sdk.return_value.status_code = 200
        self.sdk.return_value.json.return_value = {'messages': [{'id': 'wamid.exemplo123'}]}

    def finalizar(self):
        resposta = self.client.post(f'/pedidos/{self.pedido_id}/status',
            data={'status': 'Finalizado'}, follow_redirects=True)
        self.assertEqual(resposta.status_code, 200)
        with self.app.app_context():
            self.assertEqual(db.session.get(Pedido, self.pedido_id).status, 'Finalizado')
            self.assertEqual(HistoricoStatusPedido.query.count(), 1)
        for segredo in (b'AC_falso', b'segredo_falso', b'11999999999', b'21654', ('wamidexemplo123').encode()):
            self.assertNotIn(segredo, resposta.data)
        return resposta.data

    def test_aceito_texto_meta(self):
        pagina = self.finalizar()
        self.assertIn(b'flash-message sucesso', pagina)
        self.assertIn('Notifica\u00e7\u00e3o do WhatsApp disparada com sucesso!'.encode(), pagina)
        chamada = self.sdk.call_args.kwargs['json']
        self.assertIn(f'pedido #{self.pedido_id} foi finalizado', chamada['text']['body'])
        self.assertNotIn('content_sid', chamada)
        self.assertNotIn('content_variables', chamada)

    def test_falha_meta_sanitizada_preserva_finalizacao(self):
        self.sdk.side_effect = requests.ConnectionError('url_privada')
        pagina = self.finalizar()
        self.assertIn(b'flash-message erro', pagina)
        self.assertIn('N\u00e3o foi poss\u00edvel confirmar a notifica\u00e7\u00e3o'.encode(), pagina)
        self.assertNotIn(b'url_privada', pagina)

    def test_timeout_nao_afirma_que_entrega_falhou(self):
        self.sdk.side_effect = requests.Timeout('segredo_falso')
        self.assertIn('N\u00e3o foi poss\u00edvel confirmar a notifica\u00e7\u00e3o'.encode(), self.finalizar())

    def test_desativado(self):
        self.app.config['WHATSAPP_ENABLED'] = False
        self.assertIn('WhatsApp est\u00e1 desativado'.encode(), self.finalizar())
        self.sdk.assert_not_called()

    def test_telefone_invalido(self):
        with self.app.app_context():
            db.session.get(Pedido, self.pedido_id).cliente.telefone = 'invalido'
            db.session.commit()
        self.assertIn(b'verifique o telefone cadastrado', self.finalizar())
        self.sdk.assert_not_called()

    def test_configuracao_incompleta(self):
        os.environ['META_ACCESS_TOKEN'] = ''
        self.assertIn('servi\u00e7o de WhatsApp indispon\u00edvel'.encode(), self.finalizar())
        self.sdk.assert_not_called()

    def test_testing_feedback_sem_sdk(self):
        self.app.config['TESTING'] = True
        self.assertIn('Notifica\u00e7\u00e3o bloqueada no ambiente de testes'.encode(), self.finalizar())
        self.sdk.assert_not_called()

    def test_status_repetido_nao_repete_feedback_ou_envio(self):
        self.finalizar()
        self.assertNotIn('Notifica\u00e7\u00e3o do WhatsApp disparada com sucesso!'.encode(), self.finalizar())
        self.sdk.assert_called_once()

    def test_outro_status_nao_informa_envio(self):
        pagina = self.client.post(f'/pedidos/{self.pedido_id}/status',
            data={'status': 'Pronto para retirada'}, follow_redirects=True).data
        self.assertNotIn(b'Solicitacao de notificacao', pagina)
        self.sdk.assert_not_called()

    def test_sem_telefone(self):
        with self.app.app_context():
            db.session.get(Pedido, self.pedido_id).cliente.telefone = None
            db.session.commit()
        self.assertIn(b'verifique o telefone cadastrado', self.finalizar())
        self.sdk.assert_not_called()

    def test_erro_http_exibe_flash(self):
        for codigo in (400, 500):
            with self.subTest(http=codigo):
                self.client.post(f'/pedidos/{self.pedido_id}/status', data={'status': 'Pronto para retirada'})
                self.sdk.return_value.status_code = codigo
                pagina = self.client.post(f'/pedidos/{self.pedido_id}/status', data={'status': 'Finalizado'}, follow_redirects=True).data
                self.assertIn(b'flash-message erro', pagina)
                self.assertIn(b'confirmar a notifica', pagina)
