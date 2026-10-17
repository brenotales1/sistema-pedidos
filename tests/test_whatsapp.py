"""CT42 a CT45: contrato Meta, bloqueio de rede e fixture SQLite isolada."""
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch, MagicMock
import requests
from flask import Flask
from app import create_app
from database.db import db
from models.cliente import Cliente
from models.pedido import Pedido
from services.whatsapp_service import normalizar_telefone, notificar_pedido_finalizado

WAMID = 'wamid.exemplo123'
META_ENV = {'META_ACCESS_TOKEN': 'token_ficticio', 'META_PHONE_NUMBER_ID': '123456',
            'META_TEMPLATE_NAME': '', 'META_TEMPLATE_LANG': 'pt_BR', 'META_VERIFY_TOKEN': 'verificacao_ficticia'}

class SemRedeTestCase(unittest.TestCase):
    def setUp(self):
        for alvo in ('socket.create_connection', 'socket.socket.connect', 'requests.sessions.Session.request'):
            guard = patch(alvo, side_effect=AssertionError('Rede proibida nos testes'))
            guard.start()
            self.addCleanup(guard.stop)
        ambiente = patch.dict(os.environ, META_ENV)
        ambiente.start()
        self.addCleanup(ambiente.stop)

class WhatsAppServiceTestCase(SemRedeTestCase):
    def setUp(self):
        super().setUp()
        self.app = Flask(__name__)
        self.app.config.update(TESTING=False, WHATSAPP_ENABLED=True)
        ctx = self.app.app_context()
        ctx.push()
        self.addCleanup(ctx.pop)
        self.pedido = SimpleNamespace(id=5, status='Finalizado', cliente_id=2,
            cliente=SimpleNamespace(nome='Cliente ficticio', telefone='11999999999'))
        transporte = patch('services.whatsapp_service.requests.post')
        self.http = transporte.start()
        self.addCleanup(transporte.stop)
        self.http.return_value.status_code = 200
        self.http.return_value.json.return_value = {'messages': [{'id': WAMID}]}

    def test_normalizacao(self):
        for numero, esperado in [('(11) 99999-9999', 'whatsapp:+5511999999999'),
                                 ('+5521999999999', 'whatsapp:+5521999999999'),
                                 (None, None), ('', None), ('abc', None), ('123', None)]:
            with self.subTest(numero=numero):
                self.assertEqual(normalizar_telefone(numero), esperado)

    def test_http_200_e_201_com_wamid(self):
        for codigo in (200, 201):
            with self.subTest(http=codigo):
                self.http.return_value.status_code = codigo
                resultado = notificar_pedido_finalizado(self.pedido)
                self.assertEqual(resultado.status, 'aceito')
                self.assertEqual(resultado.sid, 'wamidexemplo123')
        args, kwargs = self.http.call_args
        self.assertEqual(args, ('https://graph.facebook.com/v21.0/123456/messages',))
        self.assertEqual(kwargs['headers']['Authorization'], 'Bearer token_ficticio')
        self.assertEqual(kwargs['timeout'], 10)
        self.assertEqual(kwargs['json']['to'], '5511999999999')
        self.assertEqual(kwargs['json']['messaging_product'], 'whatsapp')
        self.assertIn('pedido #5', kwargs['json']['text']['body'])
        self.assertIn('finalizado', kwargs['json']['text']['body'])

    def test_template_com_parametros_do_pedido(self):
        with patch.dict(os.environ, {'META_TEMPLATE_NAME': 'pedido_finalizado'}):
            self.assertEqual(notificar_pedido_finalizado(self.pedido).status, 'aceito')
        payload = self.http.call_args.kwargs['json']
        self.assertEqual(payload['type'], 'template')
        self.assertNotIn('text', payload)
        template = payload['template']
        self.assertEqual(template['language'], {'code': 'pt_BR'})
        self.assertEqual(template['components'][0]['parameters'], [
            {'type': 'text', 'text': 'Cliente ficticio'}, {'type': 'text', 'text': '5'}])

    def test_template_hello_world_sem_parametros(self):
        with patch.dict(os.environ, {'META_TEMPLATE_NAME': 'hello_world'}):
            notificar_pedido_finalizado(self.pedido)
        self.assertNotIn('components', self.http.call_args.kwargs['json']['template'])

    def test_http_400_e_500(self):
        for codigo in (400, 500):
            with self.subTest(http=codigo):
                self.http.return_value.status_code = codigo
                resultado = notificar_pedido_finalizado(self.pedido)
                self.assertEqual((resultado.status, resultado.codigo_erro), ('falha', codigo))
                self.assertEqual(self.pedido.status, 'Finalizado')

    def test_erro_de_rede_e_json_invalido(self):
        for erro in (requests.Timeout('simulado'), requests.ConnectionError('simulado')):
            with self.subTest(erro=type(erro).__name__):
                self.http.side_effect = erro
                self.assertEqual(notificar_pedido_finalizado(self.pedido).status, 'falha')
        self.http.side_effect = None
        self.http.return_value.json.side_effect = ValueError('JSON invalido')
        self.assertEqual(notificar_pedido_finalizado(self.pedido).status, 'falha')

    def test_telefone_invalido_ou_ausente(self):
        for telefone in (None, '', 'invalido', '123'):
            with self.subTest(telefone=telefone):
                self.pedido.cliente.telefone = telefone
                self.assertEqual(notificar_pedido_finalizado(self.pedido).status, 'sem_destinatario')
        self.http.assert_not_called()

    def test_sem_cliente(self):
        self.pedido.cliente_id = None
        self.assertEqual(notificar_pedido_finalizado(self.pedido).status, 'sem_destinatario')
        self.http.assert_not_called()

    def test_testing_bloqueia_mesmo_com_credenciais(self):
        self.app.testing = True
        self.assertEqual(notificar_pedido_finalizado(self.pedido).status, 'bloqueado_testing')
        self.http.assert_not_called()

    def test_desabilitado(self):
        self.app.config['WHATSAPP_ENABLED'] = False
        self.assertEqual(notificar_pedido_finalizado(self.pedido).status, 'desabilitado')
        self.http.assert_not_called()

    def test_outro_status(self):
        self.pedido.status = 'Pronto para retirada'
        self.assertEqual(notificar_pedido_finalizado(self.pedido).status, 'status_incompativel')
        self.http.assert_not_called()

    def test_credenciais_ausentes(self):
        for chave in ('META_ACCESS_TOKEN', 'META_PHONE_NUMBER_ID'):
            with self.subTest(chave=chave), patch.dict(os.environ, {chave: ''}):
                self.assertEqual(notificar_pedido_finalizado(self.pedido).status, 'configuracao_invalida')
        self.http.assert_not_called()

class NotificacaoPedidoTestCase(SemRedeTestCase):
    def setUp(self):
        super().setUp()
        self.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WHATSAPP_ENABLED': True})
        self.client = self.app.test_client()
        with self.client.session_transaction() as sessao:
            sessao['usuario_id'] = 1
        with self.app.app_context():
            from models.usuario import Usuario
            usuario = Usuario(id=1, nome='Operador', email='operador@teste.local', senha_hash='teste')
            db.session.add(usuario)
            cliente = Cliente(nome='Nome atual', telefone='11999999999')
            db.session.add(cliente)
            db.session.flush()
            self.pedido = Pedido(cliente_id=cliente.id, cliente_nome='Nome historico',
                categoria='Lona', material_nome='Lona', largura_pedido_m=1,
                altura_pedido_m=1, quantidade=1, unidade_medida='m',
                largura_bobina_usada_m=3.2, orientacao='Padrao', metros_consumidos=1,
                area_total_m2=1, status='Pagamento pendente')
            db.session.add(self.pedido)
            db.session.commit()
            self.pedido_id = self.pedido.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def status(self, novo):
        return self.client.post(f'/pedidos/{self.pedido_id}/status', data={'status': novo})
