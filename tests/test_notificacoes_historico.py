"""Testes automatizados para US #10 — Notificacoes / CT46: Consulta administrativa do historico."""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from app import create_app
from database.db import db
from models.cliente import Cliente
from models.historico_status_pedido import HistoricoStatusPedido
from models.notificacao_whatsapp import NotificacaoWhatsApp
from models.pedido import Pedido
from models.usuario import Usuario


class NotificacoesHistoricoTestCase(unittest.TestCase):
    """Cobre CT46: acesso de admin, campos exibidos, filtros, paginacao, ordenacao, lista vazia e nao-envio."""

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            self.admin = Usuario(nome="Admin Notificacao", email="admin.notif@sistema.com", perfil="admin")
            self.admin.definir_senha("123456")
            self.func = Usuario(nome="Funcionario Notificacao", email="func.notif@sistema.com", perfil="funcionario")
            self.func.definir_senha("123456")
            db.session.add_all([self.admin, self.func])

            self.cliente = Cliente(nome="Cliente Notificacao", telefone="11988887777")
            db.session.add(self.cliente)
            db.session.commit()

            self.admin_id = self.admin.id
            self.func_id = self.func.id
            self.cliente_id = self.cliente.id

            pedido = Pedido(
                cliente_id=self.cliente_id,
                cliente_nome=self.cliente.nome,
                categoria="Lona",
                material_nome="Lona Branca Brilho",
                largura_pedido_m=1.0,
                altura_pedido_m=1.0,
                quantidade=1,
                unidade_medida="m",
                largura_bobina_usada_m=3.20,
                orientacao="Padrão",
                metros_consumidos=1.0,
                area_total_m2=1.0,
                status="Finalizado",
            )
            db.session.add(pedido)
            db.session.commit()
            self.pedido_id = pedido.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def logar_admin(self):
        with self.client.session_transaction() as sess:
            sess["usuario_id"] = self.admin_id
            sess["usuario_perfil"] = "admin"
            sess["usuario_nome"] = "Admin Notificacao"

    def logar_funcionario(self):
        with self.client.session_transaction() as sess:
            sess["usuario_id"] = self.func_id
            sess["usuario_perfil"] = "funcionario"
            sess["usuario_nome"] = "Funcionario Notificacao"

    def criar_notificacao_aux(self, resultado="aceito", message_sid=None, codigo_erro=None, data_hora=None):
        """Cria um HistoricoStatusPedido e uma NotificacaoWhatsApp valida."""
        hist = HistoricoStatusPedido(
            pedido_id=self.pedido_id,
            status_anterior="Pronto para retirada",
            novo_status="Finalizado",
            usuario_id=self.admin_id,
        )
        db.session.add(hist)
        db.session.flush()

        notif = NotificacaoWhatsApp(
            pedido_id=self.pedido_id,
            cliente_id=self.cliente_id,
            historico_status_id=hist.id,
            evento="pedido_finalizado",
            resultado=resultado,
            message_sid=message_sid,
            codigo_erro=codigo_erro,
        )
        if data_hora:
            notif.data_hora = data_hora
        db.session.add(notif)
        db.session.commit()
        return notif

    def test_ct46_acesso_exclusivo_administrador(self):
        """Acesso exclusivo de administrador: anonimo redireciona para login, funcionario e bloqueado."""
        # 1. Sem login -> redireciona para login
        resp_anonimo = self.client.get("/notificacoes", follow_redirects=False)
        self.assertEqual(resp_anonimo.status_code, 302)
        self.assertIn("/login", resp_anonimo.location)

        # 2. Funcionario logado -> bloqueado (redirecionado para home)
        self.logar_funcionario()
        resp_func = self.client.get("/notificacoes", follow_redirects=False)
        self.assertEqual(resp_func.status_code, 302)
        self.assertEqual(resp_func.location, "/")

        # 3. Administrador logado -> acesso liberado (200 OK)
        self.logar_admin()
        resp_admin = self.client.get("/notificacoes")
        self.assertEqual(resp_admin.status_code, 200)
        self.assertIn("Histórico de notificações".encode("utf-8"), resp_admin.data)

    def test_ct46_dados_exibidos_corretos(self):
        """Exibe cliente, pedido, data e resultado corretos na tabela."""
        data_base = datetime(2026, 11, 10, 14, 30, 0)
        with self.app.app_context():
            self.criar_notificacao_aux(
                resultado="aceito",
                message_sid="wamid.CT46TESTE",
                data_hora=data_base,
            )

        self.logar_admin()
        response = self.client.get("/notificacoes")
        self.assertEqual(response.status_code, 200)

        conteudo = response.data.decode("utf-8")
        self.assertIn("Cliente Notificacao", conteudo)
        self.assertIn(f"#{self.pedido_id}", conteudo)
        self.assertIn("10/11/2026 14:30:00", conteudo)
        self.assertIn("Envio aceito pela API", conteudo)

    def test_ct46_filtros_status(self):
        """Filtros por status retornam apenas notificacoes correspondentes."""
        with self.app.app_context():
            self.criar_notificacao_aux(resultado="aceito", message_sid="wamid.ACEITA")
            self.criar_notificacao_aux(resultado="falha", codigo_erro=500)

        self.logar_admin()

        # Filtro por 'aceito'
        resp_aceito = self.client.get("/notificacoes?status=aceito")
        self.assertEqual(resp_aceito.status_code, 200)
        conteudo_aceito = resp_aceito.data.decode("utf-8")
        self.assertIn("Envio aceito pela API", conteudo_aceito)
        self.assertNotIn("Código de erro: 500", conteudo_aceito)

        # Filtro por 'falha'
        resp_falha = self.client.get("/notificacoes?status=falha")
        self.assertEqual(resp_falha.status_code, 200)
        conteudo_falha = resp_falha.data.decode("utf-8")
        self.assertIn("Falha no envio", conteudo_falha)
        self.assertIn("Código de erro: 500", conteudo_falha)

        # Status inexistente ou vazio exibe todos
        resp_todos = self.client.get("/notificacoes?status=invalido")
        self.assertEqual(resp_todos.status_code, 200)
        conteudo_todos = resp_todos.data.decode("utf-8")
        self.assertIn("Envio aceito pela API", conteudo_todos)
        self.assertIn("Falha no envio", conteudo_todos)

    def test_ct46_paginacao_25_registros(self):
        """Paginacao divide o historico em 25 registros por pagina."""
        with self.app.app_context():
            for i in range(30):
                self.criar_notificacao_aux(
                    resultado="aceito",
                    message_sid=f"wamid.PAG{i:02d}",
                    data_hora=datetime(2026, 11, 10, 10, 0, 0) + timedelta(minutes=i),
                )

        self.logar_admin()

        # Pagina 1
        resp_p1 = self.client.get("/notificacoes")
        self.assertEqual(resp_p1.status_code, 200)
        conteudo_p1 = resp_p1.data.decode("utf-8")
        self.assertIn("Página 1 de 2", conteudo_p1)
        self.assertIn("30 registro(s)", conteudo_p1)
        self.assertIn("Próxima", conteudo_p1)
        self.assertNotIn("Anterior", conteudo_p1)

        # Pagina 2
        resp_p2 = self.client.get("/notificacoes?page=2")
        self.assertEqual(resp_p2.status_code, 200)
        conteudo_p2 = resp_p2.data.decode("utf-8")
        self.assertIn("Página 2 de 2", conteudo_p2)
        self.assertIn("Anterior", conteudo_p2)
        self.assertNotIn("Próxima", conteudo_p2)

    def test_ct46_ordenacao_decrescente(self):
        """Notificacoes sao exibidas em ordem decrescente (mais recentes primeiro)."""
        hora_antiga = datetime(2026, 11, 10, 8, 0, 0)
        hora_recente = datetime(2026, 11, 10, 12, 0, 0)
        with self.app.app_context():
            self.criar_notificacao_aux(
                resultado="aceito",
                message_sid="wamid.ANTIGA",
                data_hora=hora_antiga,
            )
            self.criar_notificacao_aux(
                resultado="falha",
                message_sid="wamid.RECENTE",
                data_hora=hora_recente,
            )

        self.logar_admin()
        response = self.client.get("/notificacoes")
        self.assertEqual(response.status_code, 200)

        conteudo = response.data.decode("utf-8")
        pos_recente = conteudo.find("12:00:00")
        pos_antiga = conteudo.find("08:00:00")
        self.assertNotEqual(pos_recente, -1)
        self.assertNotEqual(pos_antiga, -1)
        self.assertLess(pos_recente, pos_antiga, "Mais recente deve aparecer antes da mais antiga")

    def test_ct46_lista_vazia(self):
        """Lista vazia exibe mensagem informativa sem falhar."""
        self.logar_admin()
        response = self.client.get("/notificacoes")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nenhuma notificação encontrada".encode("utf-8"), response.data)

    def test_ct46_consultar_nao_envia_mensagens_nem_altera_registros(self):
        """Consultar historico nao deve enviar mensagens nem alterar registros do banco."""
        with self.app.app_context():
            self.criar_notificacao_aux(
                resultado="aceito",
                message_sid="wamid.IMUTAVEL",
            )
            total_antes = NotificacaoWhatsApp.query.count()
            dados_antes = [(n.id, n.resultado, n.message_sid) for n in NotificacaoWhatsApp.query.all()]

        self.logar_admin()

        with patch("requests.post") as mock_post, patch("requests.sessions.Session.request") as mock_req:
            mock_post.side_effect = AssertionError("Acesso HTTP indevido durante consulta ao historico")
            mock_req.side_effect = AssertionError("Acesso HTTP indevido durante consulta ao historico")

            response = self.client.get("/notificacoes")
            self.assertEqual(response.status_code, 200)
            mock_post.assert_not_called()
            mock_req.assert_not_called()

        with self.app.app_context():
            total_depois = NotificacaoWhatsApp.query.count()
            dados_depois = [(n.id, n.resultado, n.message_sid) for n in NotificacaoWhatsApp.query.all()]
            self.assertEqual(total_antes, total_depois, "Consulta nao deve alterar contagem de registros")
            self.assertEqual(dados_antes, dados_depois, "Consulta nao deve alterar conteudo das notificacoes")


if __name__ == "__main__":
    unittest.main()
