"""CT42 a CT45: contrato do conector Meta sem chamadas externas."""
import os
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch
import requests
from notificacao_base import NotificacaoMixin
from services.whatsapp_service import normalizar_telefone, notificar_pedido_finalizado


class WhatsAppTestCase(NotificacaoMixin, unittest.TestCase):
    def enviar(self, telefone="11999999999", status="Finalizado", vinculado=True):
        pedido = SimpleNamespace(id=42, status=status, cliente_id=1 if vinculado else None,
                                 cliente=SimpleNamespace(nome="Cliente Ficticio", telefone=telefone))
        with self.app.app_context():
            return notificar_pedido_finalizado(pedido)

    def test_normalizacao_e_rejeicao_de_telefones(self):
        for telefone in ("(11) 99999-9999", "+55 11 99999-9999"):
            with self.subTest(telefone=telefone):
                self.assertEqual(normalizar_telefone(telefone), "whatsapp:+5511999999999")
        for telefone in (None, "", "abc", "123", "11999999999 ramal 1", 123):
            with self.subTest(telefone=telefone):
                self.assertIsNone(normalizar_telefone(telefone))

    def test_ct42_sucesso_200_e_201_e_contrato_http(self):
        self.envio_simulado_habilitado()
        for codigo in (200, 201):
            with self.subTest(codigo=codigo):
                self.post.reset_mock()
                self.post.return_value.status_code = codigo
                resultado = self.enviar()
                self.assertEqual(resultado.status, "aceito")
                self.assertEqual(resultado.sid, "wamidTESTE123")
                self.assertIsNone(resultado.codigo_erro)
                self.post.assert_called_once()
                args, kwargs = self.post.call_args
                self.assertEqual(args, ("https://graph.facebook.com/v21.0/123456/messages",))
                self.assertEqual(kwargs["timeout"], 10)
                self.assertEqual(kwargs["headers"]["Authorization"], "Bearer token-ficticio")
                payload = kwargs["json"]
                self.assertEqual(payload["messaging_product"], "whatsapp")
                self.assertEqual(payload["to"], "5511999999999")
                self.assertEqual(payload["type"], "text")
                self.assertIn("Cliente Ficticio", payload["text"]["body"])
                self.assertIn("#42", payload["text"]["body"])
        self.rede.assert_not_called()

    def test_template_com_parametros_e_hello_world(self):
        self.envio_simulado_habilitado()
        for nome in ("pedido_finalizado", "hello_world"):
            with self.subTest(nome=nome), patch.dict(os.environ, {"META_TEMPLATE_NAME": nome}):
                self.enviar()
                payload = self.post.call_args.kwargs["json"]
                self.assertEqual(payload["type"], "template")
                self.assertEqual(payload["template"]["name"], nome)
                self.assertEqual(payload["template"]["language"], {"code": "pt_BR"})
                if nome == "hello_world":
                    self.assertNotIn("components", payload["template"])
                else:
                    parametros = payload["template"]["components"][0]["parameters"]
                    self.assertEqual([p["text"] for p in parametros], ["Cliente Ficticio", "42"])

    def test_ct43_falhas_http(self):
        self.envio_simulado_habilitado()
        for codigo in (400, 500):
            with self.subTest(codigo=codigo):
                self.post.return_value = Mock(status_code=codigo, text="Erro simulado")
                resultado = self.enviar()
                self.assertEqual(resultado.status, "falha")
                self.assertEqual(resultado.codigo_erro, codigo)
                self.assertIsNone(resultado.sid)

    def test_ct43_erros_de_rede_e_json(self):
        self.envio_simulado_habilitado()
        for erro in (requests.Timeout("simulado"), requests.ConnectionError("simulado")):
            with self.subTest(erro=type(erro).__name__):
                self.post.side_effect = erro
                self.assertEqual(self.enviar().status, "falha")
        self.post.side_effect = None
        self.post.return_value.json.side_effect = ValueError("JSON invalido")
        self.assertEqual(self.enviar().status, "falha")

    def test_ct44_sem_destinatario_nao_chama_api(self):
        self.envio_simulado_habilitado()
        for telefone in (None, "", "123", "invalido"):
            with self.subTest(telefone=telefone):
                self.assertEqual(self.enviar(telefone).status, "sem_destinatario")
        self.assertEqual(self.enviar(vinculado=False).status, "sem_destinatario")
        self.post.assert_not_called()

    def test_testing_bloqueia_mesmo_com_configuracao_valida(self):
        self.assertTrue(self.app.testing)
        self.assertEqual(self.enviar().status, "bloqueado_testing")
        self.post.assert_not_called()
        self.rede.assert_not_called()

    def test_desabilitado_status_incompativel_e_credenciais_ausentes(self):
        self.envio_simulado_habilitado()
        self.app.config["WHATSAPP_ENABLED"] = False
        self.assertEqual(self.enviar().status, "desabilitado")
        self.app.config["WHATSAPP_ENABLED"] = True
        self.assertEqual(self.enviar(status="Pronto para retirada").status, "status_incompativel")
        for chave in ("META_ACCESS_TOKEN", "META_PHONE_NUMBER_ID"):
            with self.subTest(chave=chave), patch.dict(os.environ, {chave: ""}):
                self.assertEqual(self.enviar().status, "configuracao_invalida")
        self.post.assert_not_called()

    def test_webhook_verificacao_e_recebimento_sem_confirmar_entrega(self):
        resposta = self.client.get("/webhook/whatsapp", query_string={
            "hub.mode": "subscribe", "hub.verify_token": "verificacao-ficticia",
            "hub.challenge": "desafio-teste"})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.data, b"desafio-teste")
        self.assertEqual(self.client.get("/webhook/whatsapp", query_string={
            "hub.mode": "subscribe", "hub.verify_token": "incorreto"}).status_code, 403)
        resposta = self.client.post("/webhook/whatsapp", json={"entry": []})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.data, b"EVENT_RECEIVED")
        self.post.assert_not_called()
