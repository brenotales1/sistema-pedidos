"""Integracao N:N: criacao, edicao, estorno, migracao e rollback."""
import unittest
from unittest.mock import patch
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.datastructures import MultiDict
from app import create_app, preparar_banco
from database.db import db
from models.cliente import Cliente
from models.consumo_material import ConsumoMaterial
from models.material import Material
from models.movimentacao_estoque import MovimentacaoEstoque
from models.pedido import Pedido
from models.usuario import Usuario
from services.consumo_material_service import migrar_consumos_legados


class ConsumoMaterialTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
        self.client = self.app.test_client()
        with self.app.app_context():
            usuario = Usuario(nome="Operador NN", email="nn@teste.com", perfil="admin")
            usuario.definir_senha("teste")
            cliente = Cliente(nome="Cliente NN", telefone="11999999999")
            db.session.add_all([usuario, cliente])
            db.session.commit()
            self.usuario_id = usuario.id
            self.cliente_id = cliente.id
            self.principal_id = Material.query.filter_by(codigo_barras="7890000000011").one().id
            self.extra_id = Material.query.filter(Material.id != self.principal_id).first().id
            self.terceiro_id = Material.query.filter(
                ~Material.id.in_([self.principal_id, self.extra_id])
            ).first().id
            self.saldos = {m.id: m.metros_disponiveis for m in Material.query.all()}
        with self.client.session_transaction() as sessao:
            sessao["usuario_id"] = self.usuario_id
            sessao["usuario_perfil"] = "admin"

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def dados(self, adicionais=None):
        valores = {
            "cliente_id": str(self.cliente_id), "categoria": "Lona",
            "tipo": "Lona Branca Brilho", "largura": "1", "altura": "2",
            "unidade": "m", "quantidade": "2",
        }
        data = MultiDict(valores)
        for material_id, metros in adicionais or []:
            data.add("material_adicional_id", str(material_id))
            data.add("material_adicional_metros", str(metros))
        return data

    def criar(self, adicionais=None):
        resposta = self.client.post("/pedidos/novo", data=self.dados(adicionais))
        self.assertEqual(resposta.status_code, 302)
        with self.app.app_context():
            return Pedido.query.order_by(Pedido.id.desc()).first().id

    def test_n_para_n_dois_pedidos_compartilham_dois_materiais(self):
        primeiro = self.criar([(self.extra_id, 3.5)])
        segundo = self.criar([(self.extra_id, 2)])
        with self.app.app_context():
            self.assertEqual(ConsumoMaterial.query.count(), 4)
            for pedido_id in (primeiro, segundo):
                self.assertEqual({c.material_id for c in db.session.get(Pedido, pedido_id).consumos},
                                 {self.principal_id, self.extra_id})
            self.assertEqual(len(db.session.get(Material, self.extra_id).consumos), 2)
            self.assertEqual(db.session.get(Material, self.extra_id).metros_disponiveis,
                             self.saldos[self.extra_id] - 5.5)
            self.assertEqual(MovimentacaoEstoque.query.filter_by(tipo="saida").count(), 4)

    def test_editar_substitui_consumos_e_estorna_material_removido(self):
        pedido_id = self.criar([(self.extra_id, 3)])
        resposta = self.client.post(f"/pedidos/{pedido_id}/editar",
                                   data=self.dados([(self.terceiro_id, 7)]))
        self.assertEqual(resposta.status_code, 302)
        with self.app.app_context():
            pedido = db.session.get(Pedido, pedido_id)
            self.assertEqual({c.material_id for c in pedido.consumos},
                             {self.principal_id, self.terceiro_id})
            self.assertEqual(db.session.get(Material, self.extra_id).metros_disponiveis,
                             self.saldos[self.extra_id])
            self.assertEqual(db.session.get(Material, self.principal_id).metros_disponiveis,
                             self.saldos[self.principal_id] - pedido.metros_consumidos)
            self.assertEqual(db.session.get(Material, self.terceiro_id).metros_disponiveis,
                             self.saldos[self.terceiro_id] - 7)

    def test_editar_sem_alterar_nao_duplica_vinculos_nem_consumo(self):
        pedido_id = self.criar([(self.extra_id, 3)])
        self.client.post(f"/pedidos/{pedido_id}/editar", data=self.dados([(self.extra_id, 3)]))
        with self.app.app_context():
            self.assertEqual(ConsumoMaterial.query.count(), 2)
            self.assertEqual(db.session.get(Material, self.extra_id).metros_disponiveis,
                             self.saldos[self.extra_id] - 3)
        resposta = self.client.get(f"/pedidos/{pedido_id}/editar")
        self.assertIn(b'name="material_adicional_id"', resposta.data)
        self.assertIn(b'value="3.0"', resposta.data)

    def test_cancelar_estorna_todos_e_remove_associacoes(self):
        pedido_id = self.criar([(self.extra_id, 3), (self.terceiro_id, 4)])
        self.client.post(f"/pedidos/{pedido_id}/cancelar")
        with self.app.app_context():
            self.assertEqual(Pedido.query.count(), 0)
            self.assertEqual(ConsumoMaterial.query.count(), 0)
            for material_id in (self.principal_id, self.extra_id, self.terceiro_id):
                self.assertEqual(db.session.get(Material, material_id).metros_disponiveis,
                                 self.saldos[material_id])
            self.assertEqual(MovimentacaoEstoque.query.filter_by(tipo="entrada").count(), 3)

    def test_cancelamento_bloqueado_preserva_todos_os_consumos(self):
        pedido_id = self.criar([(self.extra_id, 3)])
        with self.app.app_context():
            pedido = db.session.get(Pedido, pedido_id)
            pedido.status = "Finalizado"
            db.session.commit()
        self.client.post(f"/pedidos/{pedido_id}/cancelar")
        with self.app.app_context():
            self.assertEqual(ConsumoMaterial.query.count(), 2)
            self.assertEqual(db.session.get(Material, self.extra_id).metros_disponiveis,
                             self.saldos[self.extra_id] - 3)

    def test_adicionais_invalidos_nao_alteram_pedido_estoque_historico(self):
        invalidos = ["0", "-1", "nan", "inf", "abc", "0.001", "1e999", "999999"]
        for metros in invalidos:
            with self.subTest(metros=metros):
                self.client.post("/pedidos/novo", data=self.dados([(self.extra_id, metros)]))
                with self.app.app_context():
                    self.assertEqual(Pedido.query.count(), 0)
                    self.assertEqual(ConsumoMaterial.query.count(), 0)
                    self.assertEqual(MovimentacaoEstoque.query.count(), 0)
                    self.assertEqual(db.session.get(Material, self.principal_id).metros_disponiveis,
                                     self.saldos[self.principal_id])

    def test_material_inexistente_repetido_ou_lista_incompleta_rejeitados(self):
        casos = [
            self.dados([(999999, 1)]),
            self.dados([(self.extra_id, 1), (self.extra_id, 2)]),
            self.dados([(self.principal_id, 1)]),
            self.dados([("", 1)]),
        ]
        incompleto = self.dados()
        incompleto.add("material_adicional_id", str(self.extra_id))
        casos.append(incompleto)
        for data in casos:
            with self.subTest(data=list(data.items(multi=True))):
                self.client.post("/pedidos/novo", data=data)
                with self.app.app_context():
                    self.assertEqual(Pedido.query.count(), 0)
                    self.assertEqual(MovimentacaoEstoque.query.count(), 0)

    def test_falha_no_segundo_consumo_desfaz_primeiro(self):
        from controllers.pedido_controller import consumir_material as consumir_real
        chamadas = []
        def consumir(material, metros):
            chamadas.append(material.id)
            return consumir_real(material, metros) if len(chamadas) == 1 else False
        with patch("controllers.pedido_controller.consumir_material", side_effect=consumir):
            self.client.post("/pedidos/novo", data=self.dados([(self.extra_id, 3)]))
        with self.app.app_context():
            self.assertEqual(Pedido.query.count(), 0)
            self.assertEqual(MovimentacaoEstoque.query.count(), 0)
            self.assertEqual(db.session.get(Material, self.principal_id).metros_disponiveis,
                             self.saldos[self.principal_id])

    def test_falha_commit_edicao_preserva_pedido_consumos_saldos_historico(self):
        pedido_id = self.criar([(self.extra_id, 3)])
        with self.app.app_context():
            quantidade_movimentos = MovimentacaoEstoque.query.count()
        with patch.object(db.session, "commit", side_effect=SQLAlchemyError("falha simulada")):
            self.client.post(f"/pedidos/{pedido_id}/editar",
                             data=self.dados([(self.terceiro_id, 4)]))
        with self.app.app_context():
            self.assertEqual({c.material_id for c in db.session.get(Pedido, pedido_id).consumos},
                             {self.principal_id, self.extra_id})
            self.assertEqual(MovimentacaoEstoque.query.count(), quantidade_movimentos)
            self.assertEqual(db.session.get(Material, self.terceiro_id).metros_disponiveis,
                             self.saldos[self.terceiro_id])
            self.assertEqual(db.session.get(Material, self.extra_id).metros_disponiveis,
                             self.saldos[self.extra_id] - 3)

    def test_material_associado_nao_pode_ser_excluido_mesmo_sem_movimentacao(self):
        self.criar([(self.extra_id, 3)])
        with self.app.app_context():
            MovimentacaoEstoque.query.delete()
            db.session.commit()
        self.client.post(f"/estoque/material/{self.extra_id}/excluir")
        with self.app.app_context():
            self.assertIsNotNone(db.session.get(Material, self.extra_id))
            self.assertEqual(ConsumoMaterial.query.count(), 2)

    def test_detalhe_busca_e_cancelamento_usam_id_mesmo_apos_renomear(self):
        pedido_id = self.criar([(self.extra_id, 3)])
        with self.app.app_context():
            db.session.get(Material, self.extra_id).nome = "Complemento especial NN"
            db.session.get(Material, self.principal_id).nome = "Principal renomeado"
            db.session.commit()
        resposta = self.client.get(f"/pedidos/{pedido_id}")
        self.assertIn(b"Complemento especial NN", resposta.data)
        resposta = self.client.get("/pedidos?filtro=material&busca=Complemento+especial+NN")
        self.assertIn(f"/pedidos/{pedido_id}".encode(), resposta.data)
        self.client.post(f"/pedidos/{pedido_id}/cancelar")
        with self.app.app_context():
            self.assertEqual(db.session.get(Material, self.principal_id).metros_disponiveis,
                             self.saldos[self.principal_id])

    def test_migracao_legada_idempotente_sem_baixa_e_reinicio_preserva(self):
        pedido_id = self.criar()
        with self.app.app_context():
            pedido = db.session.get(Pedido, pedido_id)
            consumo_original = pedido.metros_consumidos
            saldo = db.session.get(Material, self.principal_id).metros_disponiveis
            movimentos = MovimentacaoEstoque.query.count()
            pedido.consumos.clear()
            db.session.execute(text("DELETE FROM schema_migration WHERE nome = 'pedido_consumo_material_v1'"))
            db.session.commit()
            ConsumoMaterial.__table__.drop(bind=db.engine)
            db.session.expire_all()
            preparar_banco(self.app)
            migrar_consumos_legados()
            preparar_banco(self.app)
            self.assertEqual(ConsumoMaterial.query.count(), 1)
            self.assertEqual(ConsumoMaterial.query.one().quantidade_metros, consumo_original)
            self.assertEqual(db.session.get(Material, self.principal_id).metros_disponiveis, saldo)
            self.assertEqual(MovimentacaoEstoque.query.count(), movimentos)

    def test_edicao_invalida_preserva_consumos_anteriores(self):
        pedido_id = self.criar([(self.extra_id, 3)])
        resposta = self.client.post(f"/pedidos/{pedido_id}/editar",
                                   data=self.dados([(self.terceiro_id, 999999)]))
        self.assertEqual(resposta.status_code, 200)
        with self.app.app_context():
            self.assertEqual({c.material_id for c in db.session.get(Pedido, pedido_id).consumos},
                             {self.principal_id, self.extra_id})
            self.assertEqual(db.session.get(Material, self.extra_id).metros_disponiveis,
                             self.saldos[self.extra_id] - 3)
            self.assertEqual(MovimentacaoEstoque.query.count(), 2)

    def test_falha_commit_cancelamento_desfaz_todos_os_estornos(self):
        pedido_id = self.criar([(self.extra_id, 3)])
        with patch.object(db.session, "commit", side_effect=SQLAlchemyError("falha")):
            self.client.post(f"/pedidos/{pedido_id}/cancelar")
        with self.app.app_context():
            self.assertIsNotNone(db.session.get(Pedido, pedido_id))
            self.assertEqual(ConsumoMaterial.query.count(), 2)
            self.assertEqual(MovimentacaoEstoque.query.count(), 2)
            self.assertEqual(db.session.get(Material, self.extra_id).metros_disponiveis,
                             self.saldos[self.extra_id] - 3)

    def test_legado_sem_material_identificavel_nao_e_associado_nem_estornado(self):
        pedido_id = self.criar()
        with self.app.app_context():
            pedido = db.session.get(Pedido, pedido_id)
            pedido.consumos.clear()
            pedido.material_nome = "Material antigo inexistente"
            db.session.execute(text("DELETE FROM schema_migration WHERE nome = 'pedido_consumo_material_v1'"))
            db.session.commit()
            migrar_consumos_legados()
            self.assertEqual(ConsumoMaterial.query.count(), 0)
            self.assertEqual(db.session.get(Pedido, pedido_id).material_nome,
                             "Material antigo inexistente")
        self.client.post(f"/pedidos/{pedido_id}/cancelar")
        with self.app.app_context():
            self.assertIsNotNone(db.session.get(Pedido, pedido_id))
            self.assertEqual(MovimentacaoEstoque.query.count(), 1)

    def test_constraints_impedem_consumo_zero_e_vinculo_duplicado(self):
        pedido_id = self.criar()
        with self.app.app_context():
            for material_id, metros in [(self.extra_id, 0), (self.principal_id, 1)]:
                with self.subTest(material_id=material_id):
                    db.session.execute(text("SELECT 1"))
                    db.session.add(ConsumoMaterial(
                        pedido_id=pedido_id, material_id=material_id,
                        quantidade_metros=metros, principal=False,
                    ))
                    with self.assertRaises(IntegrityError):
                        db.session.commit()
                    db.session.rollback()
            self.assertEqual(ConsumoMaterial.query.count(), 1)


if __name__ == "__main__":
    unittest.main()
