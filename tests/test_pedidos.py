"""Testes automatizados para o modulo de pedidos e algoritmo de aproveitamento de corte."""

import unittest
from app import create_app
from database.db import db
from models.cliente import Cliente
from models.material import Material
from models.pedido import Pedido
from models.usuario import Usuario
from services.estoque_service import adicionar_bobina
from services.pedido_service import (
    calcular_melhor_aproveitamento,
    converter_para_metros,
    formatar_area,
    formatar_metros,
)


class PedidosTestCase(unittest.TestCase):
    """Casos de teste para criacao, calculo de corte e ciclo de vida de pedidos."""

    def setUp(self):
        """Configura banco em memoria com materiais e cliente de teste."""
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            # Cria usuario se nao existir
            user = Usuario.query.filter_by(email="func@sistema.com").first()
            if not user:
                user = Usuario(nome="Funcionario", email="func@sistema.com", perfil="funcionario")
                user.definir_senha("123456")
                db.session.add(user)

            # Cria cliente
            cliente = Cliente.query.filter_by(nome="Cliente Teste").first()
            if not cliente:
                cliente = Cliente(nome="Cliente Teste", telefone="11999999999", empresa="Empresa XYZ")
                db.session.add(cliente)

            db.session.commit()
            self.cliente_id = cliente.id

        self.client.post("/login", data={"email": "func@sistema.com", "senha": "123456"})

    def tearDown(self):
        """Limpa o banco ao final de cada teste."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def dados_pedido(self, cliente_id):
        return {"cliente_id": str(cliente_id), "categoria": "Lona",
                "tipo": "Lona Branca Brilho", "largura": "1", "altura": "2",
                "unidade": "m", "quantidade": "2"}

    def test_cliente_invalido_nao_baixa_estoque(self):
        for valor in ('invalido', '99999', ''):
            response = self.client.post('/pedidos/novo', data=self.dados_pedido(valor))
            self.assertIn('Selecione um cliente'.encode(), response.data)
        with self.app.app_context():
            self.assertEqual(Pedido.query.count(), 0)
            self.assertEqual(Material.query.filter_by(codigo_barras='7890000000011').first().metros_disponiveis, 50)

    def test_homonimos_selecionados_por_id_e_historico_preservado(self):
        with self.app.app_context():
            outro = Cliente(nome='Cliente Teste', telefone='11888888888')
            db.session.add(outro)
            db.session.commit()
            outro_id = outro.id
        response = self.client.post('/pedidos/novo', data=self.dados_pedido(outro_id))
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            pedido = Pedido.query.one()
            pedido_id = pedido.id
            self.assertEqual(pedido.cliente_id, outro_id)
            pedido.cliente.nome = 'Nome atualizado'
            db.session.commit()
        response = self.client.get(f'/pedidos/{pedido_id}/editar')
        self.assertIn(f'value="{outro_id}" selected'.encode(), response.data)
        self.client.post(f'/pedidos/{pedido_id}/editar', data=self.dados_pedido(outro_id))
        with self.app.app_context():
            self.assertEqual(Pedido.query.one().cliente_nome, 'Cliente Teste')
        self.client.post(f'/pedidos/{pedido_id}/editar', data=self.dados_pedido(self.cliente_id))
        with self.app.app_context():
            self.assertEqual(Pedido.query.one().cliente_id, self.cliente_id)

    def test_legado_editavel_sem_associacao_e_vinculo_explicito(self):
        self.client.post('/pedidos/novo', data=self.dados_pedido(self.cliente_id))
        with self.app.app_context():
            pedido = Pedido.query.one()
            pedido.cliente_id = None
            pedido.cliente_nome = 'Historico sem cadastro'
            pedido_id = pedido.id
            db.session.commit()
        response = self.client.get(f'/pedidos/{pedido_id}/editar')
        self.assertIn('Manter sem vínculo'.encode(), response.data)
        self.client.post(f'/pedidos/{pedido_id}/editar', data=self.dados_pedido(''))
        with self.app.app_context():
            pedido = Pedido.query.one()
            self.assertIsNone(pedido.cliente_id)
            self.assertEqual(pedido.cliente_nome, 'Historico sem cadastro')
        self.client.post(f'/pedidos/{pedido_id}/editar', data=self.dados_pedido(self.cliente_id))
        with self.app.app_context():
            self.assertEqual(Pedido.query.one().cliente_id, self.cliente_id)

    def test_conversao_medidas(self):
        """Testa conversao de centimetros e metros para metros com precisao."""
        self.assertEqual(converter_para_metros("150", "cm"), 1.50)
        self.assertEqual(converter_para_metros("2.5", "m"), 2.50)
        self.assertEqual(converter_para_metros("2,5", "m"), 2.50)

    def test_calculo_aproveitamento_corte_padrao_e_rotacionado(self):
        """Testa o algoritmo de orientacao ideal para minimizar o desperdicio."""
        with self.app.app_context():
            variacoes = Material.query.filter_by(categoria="Lona", nome="Lona Branca Brilho").all()

            # Pedido: 1.00m de largura por 2.00m de altura, 2 unidades
            # Na bobina de 3.20m, o algoritmo rotaciona (1.00m na bobina x 2 un = 2.00m consumidos)
            sugestao = calcular_melhor_aproveitamento(
                variacoes=variacoes,
                largura_m=1.00,
                altura_m=2.00,
                quantidade=2,
            )
            self.assertIsNotNone(sugestao)
            self.assertEqual(sugestao["largura_bobina"], 3.20)
            self.assertEqual(sugestao["orientacao"], "Rotacionado")
            self.assertEqual(sugestao["metros_consumidos"], 2.00)

    def test_fluxo_criacao_pedido_com_baixa_estoque(self):
        """Criar um novo pedido baixa a metragem do material automaticamente."""
        response = self.client.post(
            "/pedidos/novo",
            data={
                "cliente_id": str(self.cliente_id),
                "categoria": "Lona",
                "tipo": "Lona Branca Brilho",
                "largura": "1.00",
                "altura": "2.00",
                "unidade": "m",
                "quantidade": "2",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            pedido = Pedido.query.filter_by(cliente_nome="Cliente Teste").first()
            self.assertIsNotNone(pedido)
            self.assertEqual(pedido.metros_consumidos, 2.00)
            self.assertEqual(pedido.status, "Pagamento pendente")
            self.assertEqual(pedido.cliente_id, self.cliente_id)
            self.assertEqual(pedido.cliente.id, self.cliente_id)

            # Verifica estoque restante (50 - 2 = 48)
            mat = Material.query.filter_by(codigo_barras="7890000000011").first()
            self.assertEqual(mat.metros_disponiveis, 48.00)

    def test_cancelamento_pedido_estorna_estoque(self):
        """Cancelar um pedido deve excluir o registro e estornar a metragem ao estoque."""
        # Cria pedido
        self.client.post(
            "/pedidos/novo",
            data={
                "cliente_id": str(self.cliente_id),
                "categoria": "Lona",
                "tipo": "Lona Branca Brilho",
                "largura": "1.00",
                "altura": "2.00",
                "unidade": "m",
                "quantidade": "2",
            },
        )

        with self.app.app_context():
            pedido = Pedido.query.filter_by(cliente_nome="Cliente Teste").first()
            pedido_id = pedido.id

        # Cancela pedido
        response = self.client.post(f"/pedidos/{pedido_id}/cancelar", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            pedido_cancelado = Pedido.query.get(pedido_id)
            self.assertIsNone(pedido_cancelado)

            # Metragem deve retornar para 50.00
            mat = Material.query.filter_by(codigo_barras="7890000000011").first()
            self.assertEqual(mat.metros_disponiveis, 50.00)

    def test_atualizar_status_pedido(self):
        """Atualizacao de status do pedido reflete no banco."""
        with self.app.app_context():
            pedido = Pedido(
                cliente_id=self.cliente_id,
                cliente_nome="Cliente Teste",
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
                status="Pagamento pendente",
            )
            db.session.add(pedido)
            db.session.commit()
            pedido_id = pedido.id

        response = self.client.post(
            f"/pedidos/{pedido_id}/status",
            data={"status": "Pronto para retirada"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            pedido_atualizado = Pedido.query.get(pedido_id)
            self.assertEqual(pedido_atualizado.status, "Pronto para retirada")


if __name__ == "__main__":
    unittest.main()
