"""CT43 / US #9 (CT09 de notificacoes na retrospectiva): persistencia e unicidade sem banco local ou rede."""
import unittest
from datetime import datetime, timezone
from unittest.mock import patch
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from tests import test_whatsapp as whatsapp_tests
from database.db import db
from models.pedido import Pedido
from models.notificacao_whatsapp import NotificacaoWhatsApp
from services.database_migration_service import garantir_tabela_notificacao_whatsapp
from services.pedido_service import registrar_resultado_notificacao
from services.whatsapp_service import ResultadoEnvio
import requests
import os


class NotificacaoPersistenciaTestCase(unittest.TestCase):
    def setUp(self):
        self.fixture = whatsapp_tests.NotificacaoPedidoTestCase()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.app = self.fixture.app
        self.client = self.fixture.client
        self.pedido_id = self.fixture.pedido_id
        self.app.config.update(TESTING=False)
        guard = patch('services.whatsapp_service.requests.post')
        self.sdk = guard.start()
        self.addCleanup(guard.stop)
        self.sdk.return_value.status_code = 200
        self.sdk.return_value.json.return_value = {'messages': [{'id': 'wamid.exemplo123'}]}

    def alterar(self, status='Finalizado'):
        self.assertEqual(self.client.post(f'/pedidos/{self.pedido_id}/status',
            data={'status': status}).status_code, 302)

    def registro(self, resultado):
        db.session.remove()
        linha = NotificacaoWhatsApp.query.one()
        self.assertEqual(linha.resultado, resultado)
        self.assertFalse(linha.entrega_confirmada)
        self.assertEqual(db.session.get(Pedido, self.pedido_id).status, 'Finalizado')
        return linha

    def test_aceito_campos_utc_e_cliente_correto(self):
        antes = datetime.now(timezone.utc).replace(tzinfo=None)
        self.alterar()
        with self.app.app_context():
            linha = self.registro('aceito')
            self.assertEqual(linha.pedido_id, self.pedido_id)
            self.assertEqual(linha.cliente_id, linha.pedido.cliente_id)
            self.assertEqual(linha.evento, 'pedido_finalizado')
            self.assertEqual(linha.historico_status.novo_status, 'Finalizado')
            self.assertGreaterEqual(linha.data_hora, antes)
            self.assertLessEqual(linha.data_hora, datetime.now(timezone.utc).replace(tzinfo=None))
            self.assertEqual(linha.message_sid, 'wamidexemplo123')
            self.assertIsNone(linha.codigo_erro)

    def test_telefone_invalido(self):
        with self.app.app_context():
            db.session.get(Pedido, self.pedido_id).cliente.telefone = 'invalido'
            db.session.commit()
        self.alterar()
        with self.app.app_context():
            self.registro('sem_destinatario')
        self.sdk.assert_not_called()

    def test_configuracao_invalida(self):
        os.environ['META_ACCESS_TOKEN'] = ''
        self.alterar()
        with self.app.app_context():
            self.registro('configuracao_invalida')
        self.sdk.assert_not_called()

    def test_falha_meta_codigo_sem_dados_sensiveis(self):
        self.sdk.return_value.status_code = 400
        self.alterar()
        with self.app.app_context():
            linha = self.registro('falha')
            self.assertEqual(linha.codigo_erro, 400)
            self.assertIsNone(linha.message_sid)
            valores = str({c.name: getattr(linha, c.name) for c in linha.__table__.columns})
            for segredo in ('url_privada', 'token_privado', 'telefone_privado', 'segredo_falso'):
                self.assertNotIn(segredo, valores)

    def test_timeout_preserva_finalizado(self):
        self.sdk.side_effect = requests.Timeout('segredo')
        self.alterar()
        with self.app.app_context():
            self.assertIsNone(self.registro('falha').codigo_erro)

    def test_desabilitado_e_testing(self):
        self.app.config['WHATSAPP_ENABLED'] = False
        self.alterar()
        with self.app.app_context():
            self.registro('desabilitado')
        self.alterar('Pronto para retirada')
        self.app.config['TESTING'] = True
        self.alterar()
        with self.app.app_context():
            self.assertEqual([n.resultado for n in NotificacaoWhatsApp.query.order_by(NotificacaoWhatsApp.id)],
                ['desabilitado', 'bloqueado_testing'])
        self.sdk.assert_not_called()

    def test_repeticao_outros_status_e_nova_transicao(self):
        self.alterar('Pronto para retirada')
        with self.app.app_context():
            self.assertEqual(NotificacaoWhatsApp.query.count(), 0)
        self.alterar()
        self.alterar()
        with self.app.app_context():
            self.registro('aceito')
        self.sdk.assert_called_once()
        self.alterar('Pronto para retirada')
        self.alterar()
        with self.app.app_context():
            self.assertEqual(NotificacaoWhatsApp.query.count(), 2)
        self.assertEqual(self.sdk.call_count, 2)

    def test_mesma_tentativa_atualizada_sem_duplicar(self):
        self.alterar()
        with self.app.app_context():
            linha = self.registro('aceito')
            registrar_resultado_notificacao(linha, ResultadoEnvio('aceito', sid='wamidexemplo123'))
            self.assertEqual(NotificacaoWhatsApp.query.count(), 1)
            duplicado = NotificacaoWhatsApp(historico_status_id=linha.historico_status_id,
                pedido_id=linha.pedido_id, cliente_id=linha.cliente_id)
            db.session.add(duplicado)
            with self.assertRaises(IntegrityError):
                db.session.commit()
            db.session.rollback()
        self.sdk.assert_called_once()

    def test_falha_gravacao_resultado_preserva_pendente_e_finalizacao(self):
        def falhar(*args):
            raise RuntimeError('segredo')
        event.listen(NotificacaoWhatsApp, 'before_update', falhar)
        try:
            self.alterar()
        finally:
            event.remove(NotificacaoWhatsApp, 'before_update', falhar)
        with self.app.app_context():
            self.registro('pendente')
        self.alterar()
        self.sdk.assert_called_once()

    def test_migracao_reexecutavel_preserva_dados(self):
        with self.app.app_context():
            NotificacaoWhatsApp.__table__.drop(db.engine)
            garantir_tabela_notificacao_whatsapp()
        self.alterar()
        with self.app.app_context():
            garantir_tabela_notificacao_whatsapp()
            garantir_tabela_notificacao_whatsapp()
            self.registro('aceito')
            self.assertEqual(Pedido.query.count(), 1)

    def test_ct43_us09_destinatario_por_id_entre_homonimos(self):
        from models.cliente import Cliente
        with self.app.app_context():
            pedido = db.session.get(Pedido, self.pedido_id)
            # Outro cadastro com o mesmo nome: o nome historico nao decide o envio.
            outro = Cliente(nome=pedido.cliente.nome, telefone='21999999999')
            db.session.add(outro)
            db.session.flush()
            pedido.cliente_id = outro.id
            cliente_id = outro.id
            db.session.commit()
        self.alterar()
        chamada = self.sdk.call_args.kwargs['json']
        self.assertEqual(chamada['to'], '5521999999999')
        self.assertIn(f'pedido #{self.pedido_id} foi finalizado', chamada['text']['body'])
        with self.app.app_context():
            self.assertEqual(self.registro('aceito').cliente_id, cliente_id)

    def test_ct43_us09_todos_status_e_repeticao_sem_rede(self):
        from services.constantes import STATUS_PEDIDO
        import socket
        import requests
        for status in STATUS_PEDIDO:
            if status == 'Finalizado':
                continue
            with self.subTest(status=status):
                self.alterar(status)
                self.alterar(status)
                with self.app.app_context():
                    self.assertEqual(NotificacaoWhatsApp.query.count(), 0)
                self.sdk.assert_not_called()
        self.alterar()
        self.alterar()
        self.sdk.assert_called_once()
        with self.app.app_context():
            self.registro('aceito')
        # As protecoes de transporte herdadas da fixture nao foram acionadas.
        socket.create_connection.assert_not_called()
        socket.socket.connect.assert_not_called()
        requests.sessions.Session.request.assert_not_called()

    def test_http_201_persiste_aceito(self):
        self.sdk.return_value.status_code = 201
        self.alterar()
        with self.app.app_context():
            self.assertEqual(self.registro('aceito').message_sid, 'wamidexemplo123')

    def test_http_500_persiste_falha(self):
        self.sdk.return_value.status_code = 500
        self.alterar()
        with self.app.app_context():
            self.assertEqual(self.registro('falha').codigo_erro, 500)

    def test_commit_da_transicao_antes_do_envio(self):
        def responder(*args, **kwargs):
            self.assertFalse(db.session.dirty)
            self.assertEqual(db.session.get(Pedido, self.pedido_id).status, 'Finalizado')
            self.assertEqual(NotificacaoWhatsApp.query.one().resultado, 'pendente')
            from unittest.mock import Mock
            return Mock(status_code=200, json=lambda: {'messages': [{'id': 'wamid.exemplo123'}]})
        self.sdk.side_effect = responder
        self.alterar()
        self.sdk.assert_called_once()
        with self.app.app_context():
            self.registro('aceito')

    def test_webhook_verificacao_e_recebimento(self):
        for token, codigo in [('verificacao_ficticia', 200), ('incorreto', 403)]:
            resposta = self.client.get('/webhook/whatsapp', query_string={
                'hub.mode': 'subscribe', 'hub.verify_token': token, 'hub.challenge': 'desafio'})
            self.assertEqual(resposta.status_code, codigo)
            if codigo == 200:
                self.assertEqual(resposta.data, b'desafio')
        self.assertEqual(self.client.post('/webhook/whatsapp', json={'entry': []}).status_code, 200)
        self.sdk.assert_not_called()
