"""Infraestrutura isolada para os testes de notificacao da Sprint 3."""
import os
from unittest.mock import patch, Mock
from app import create_app
from database.db import db
from models.cliente import Cliente
from models.pedido import Pedido
from models.usuario import Usuario


class NotificacaoMixin:
    def setUp(self):
        # Nunca herdar credenciais reais carregadas do .env.
        ambiente = patch.dict(os.environ, {
            "META_ACCESS_TOKEN": "token-ficticio",
            "META_PHONE_NUMBER_ID": "123456",
            "META_TEMPLATE_NAME": "",
            "META_TEMPLATE_LANG": "pt_BR",
            "META_VERIFY_TOKEN": "verificacao-ficticia",
        })
        ambiente.start()
        self.addCleanup(ambiente.stop)
        # Segunda barreira: qualquer HTTP nao previsto falha antes da rede.
        rede = patch("requests.sessions.Session.request",
                     side_effect=AssertionError("Acesso real a rede proibido"))
        self.rede = rede.start()
        self.addCleanup(rede.stop)
        post = patch("services.whatsapp_service.requests.post")
        self.post = post.start()
        self.addCleanup(post.stop)
        self.post.return_value = Mock(
            status_code=200, json=Mock(return_value={"messages": [{"id": "wamid.TESTE123"}]}))
        self.app = create_app({
            "TESTING": True, "SECRET_KEY": "chave-ficticia",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WHATSAPP_ENABLED": True,
        })
        self.addCleanup(self.limpar_banco)
        self.client = self.app.test_client()
        with self.app.app_context():
            cliente = Cliente(nome="Cliente Ficticio", telefone="11999999999")
            usuario = Usuario(nome="Operador Teste", email="operador@example.test",
                              perfil="funcionario", senha_hash="hash-ficticio")
            db.session.add_all([cliente, usuario])
            db.session.flush()
            pedido = Pedido(
                cliente_id=cliente.id, cliente_nome=cliente.nome, categoria="Lona",
                material_nome="Lona Branca Brilho", largura_pedido_m=1,
                altura_pedido_m=1, quantidade=1, unidade_medida="m",
                largura_bobina_usada_m=3.2, orientacao="Padrao",
                metros_consumidos=1, area_total_m2=1, status="Pronto para retirada")
            db.session.add(pedido)
            db.session.commit()
            self.pedido_id, self.cliente_id, self.usuario_id = pedido.id, cliente.id, usuario.id
        with self.client.session_transaction() as sessao:
            sessao["usuario_id"] = self.usuario_id
            sessao["usuario_perfil"] = "funcionario"

    def limpar_banco(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def finalizar(self, status="Finalizado"):
        return self.client.post(f"/pedidos/{self.pedido_id}/status",
                                data={"status": status}, follow_redirects=True)

    def envio_simulado_habilitado(self):
        # Somente apos instalar o mock e a barreira de rede.
        self.app.testing = False
