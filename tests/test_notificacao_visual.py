"""CT42 a CT44: feedback HTTP e flash para o operador."""
import unittest
import requests
from notificacao_base import NotificacaoMixin
from database.db import db
from models.cliente import Cliente
from models.pedido import Pedido
from models.notificacao_whatsapp import NotificacaoWhatsApp


class NotificacaoVisualTestCase(NotificacaoMixin, unittest.TestCase):
    def verificar(self, resposta, texto, categoria, resultado):
        self.assertEqual(resposta.status_code, 200)
        html = resposta.get_data(as_text=True)
        self.assertIn(texto, html)
        self.assertIn(f"flash-message {categoria}", html)
        with self.app.app_context():
            self.assertEqual(db.session.get(Pedido, self.pedido_id).status, "Finalizado")
            self.assertEqual(NotificacaoWhatsApp.query.one().resultado, resultado)

    def test_ct42_flash_sucesso_e_persistencia(self):
        self.envio_simulado_habilitado()
        self.verificar(self.finalizar(), "Notificação do WhatsApp disparada com sucesso!",
                       "sucesso", "aceito")
        self.post.assert_called_once()

    def test_ct43_flash_falha_api_preserva_pedido(self):
        self.envio_simulado_habilitado()
        self.post.return_value.status_code = 500
        self.verificar(self.finalizar(), "Não foi possível confirmar a notificação",
                       "erro", "falha")

    def test_ct43_flash_erro_rede_preserva_pedido(self):
        self.envio_simulado_habilitado()
        self.post.side_effect = requests.Timeout("simulado")
        self.verificar(self.finalizar(), "Não foi possível confirmar a notificação",
                       "erro", "falha")

    def test_ct44_flash_telefone_invalido(self):
        self.envio_simulado_habilitado()
        with self.app.app_context():
            db.session.get(Cliente, self.cliente_id).telefone = "123"
            db.session.commit()
        self.verificar(self.finalizar(), "verifique o telefone cadastrado do cliente",
                       "erro", "sem_destinatario")
        self.post.assert_not_called()

    def test_ct44_flash_telefone_ausente(self):
        self.envio_simulado_habilitado()
        with self.app.app_context():
            db.session.get(Cliente, self.cliente_id).telefone = None
            db.session.commit()
        self.verificar(self.finalizar(), "verifique o telefone cadastrado do cliente",
                       "erro", "sem_destinatario")
        self.post.assert_not_called()

    def test_flash_bloqueio_testing_sem_http(self):
        self.verificar(self.finalizar(), "Notificação bloqueada no ambiente de testes",
                       "info", "bloqueado_testing")
        self.post.assert_not_called()
        self.rede.assert_not_called()
