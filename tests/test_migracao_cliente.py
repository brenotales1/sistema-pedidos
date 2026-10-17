"""Migracao legada testada sem abrir o banco da aplicacao."""
import unittest
from unittest.mock import patch
from flask import Flask
from sqlalchemy import inspect, text
from database.db import db
from services.database_migration_service import migrar_cliente_id_pedido


class MigracaoClienteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        db.init_app(self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()
        with db.engine.begin() as c:
            c.exec_driver_sql("CREATE TABLE cliente (id INTEGER PRIMARY KEY, nome TEXT)")
            c.exec_driver_sql("CREATE TABLE pedido (id INTEGER PRIMARY KEY, cliente_nome TEXT, status TEXT)")
            c.exec_driver_sql("INSERT INTO cliente VALUES (1, 'Unico'), (2, 'Duplicado'), (3, 'Duplicado')")
            c.exec_driver_sql("INSERT INTO pedido VALUES (1, 'Unico', 'Finalizado'), (2, 'Duplicado', 'Pendente'), (3, 'Ausente', 'Pendente'), (4, 'unico', 'Pendente')")

    def tearDown(self):
        db.session.remove()
        db.engine.dispose()
        self.ctx.pop()

    def test_associa_apenas_nome_exato_unico_e_preserva_dados(self):
        migrar_cliente_id_pedido()
        with db.engine.connect() as c:
            rows = c.execute(text("SELECT id, cliente_nome, status, cliente_id FROM pedido ORDER BY id")).all()
            self.assertEqual(rows, [(1, 'Unico', 'Finalizado', 1), (2, 'Duplicado', 'Pendente', None), (3, 'Ausente', 'Pendente', None), (4, 'unico', 'Pendente', None)])
            fk = inspect(c).get_foreign_keys('pedido')[0]
            self.assertEqual(fk['referred_table'], 'cliente')
            self.assertTrue(next(x for x in inspect(c).get_columns('pedido') if x['name'] == 'cliente_id')['nullable'])

    def test_reexecucao_nao_reassocia_pedidos_pendentes(self):
        migrar_cliente_id_pedido()
        with db.engine.begin() as c:
            c.exec_driver_sql("DELETE FROM cliente WHERE id = 3")
            c.exec_driver_sql("INSERT INTO cliente VALUES (4, 'Ausente')")
        migrar_cliente_id_pedido()
        with db.engine.connect() as c:
            self.assertEqual(c.exec_driver_sql("SELECT cliente_id FROM pedido ORDER BY id").scalars().all(), [1, None, None, None])
            self.assertEqual(c.exec_driver_sql("SELECT COUNT(*) FROM schema_migration").scalar(), 1)

    def test_falha_reverte_coluna_dados_e_marcador(self):
        from sqlalchemy.engine import Connection
        original = Connection.execute
        def falhar(conexao, statement, *args, **kwargs):
            if str(statement).startswith('INSERT INTO schema_migration'):
                raise RuntimeError('falha simulada')
            return original(conexao, statement, *args, **kwargs)
        with patch.object(Connection, 'execute', falhar):
            with self.assertRaises(RuntimeError):
                migrar_cliente_id_pedido()
        self.assertNotIn('cliente_id', [c['name'] for c in inspect(db.engine).get_columns('pedido')])
        migrar_cliente_id_pedido()
        self.assertIn('cliente_id', [c['name'] for c in inspect(db.engine).get_columns('pedido')])
