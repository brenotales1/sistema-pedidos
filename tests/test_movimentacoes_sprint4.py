"""Testes automatizados para US #6 — Movimentacoes de estoque, alteracoes manuais e consistencia do historico."""

import unittest
from app import create_app
from database.db import db
from models.bobina_estoque import BobinaEstoque
from models.cliente import Cliente
from models.material import Material
from models.movimentacao_estoque import MovimentacaoEstoque
from models.pedido import Pedido
from models.usuario import Usuario
from services.constantes import METROS_POR_BOBINA
from services.estoque_service import (
    adicionar_bobina,
    listar_movimentacoes,
    registrar_entrada_estoque,
    registrar_movimentacao,
)


class MovimentacoesEstoqueTestCase(unittest.TestCase):
    """Cobre US #6: criacao, edicao e cancelamento de pedidos, alteracoes manuais e consistencia do historico."""

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            # Cria administrador e funcionario
            self.admin = Usuario(nome="Admin Teste", email="admin@sistema.com", perfil="admin")
            self.admin.definir_senha("123456")
            self.func = Usuario(nome="Funcionario Teste", email="func@sistema.com", perfil="funcionario")
            self.func.definir_senha("123456")
            db.session.add_all([self.admin, self.func])

            # Cria cliente
            self.cliente = Cliente(nome="Cliente Movimentacoes", telefone="11999998888")
            db.session.add(self.cliente)
            db.session.commit()

            self.admin_id = self.admin.id
            self.func_id = self.func.id
            self.cliente_id = self.cliente.id

            # Material base
            self.mat = Material.query.filter_by(codigo_barras="7890000000011").first()
            if self.mat and len(self.mat.bobinas) < 2:
                adicionar_bobina(self.mat, 2 - len(self.mat.bobinas))
                db.session.commit()
            self.material_id = self.mat.id

        # Login como administrador por padrao
        self.logar_admin()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def logar_admin(self):
        with self.client.session_transaction() as sess:
            sess["usuario_id"] = self.admin_id
            sess["usuario_perfil"] = "admin"
            sess["usuario_nome"] = "Admin Teste"

    def logar_funcionario(self):
        with self.client.session_transaction() as sess:
            sess["usuario_id"] = self.func_id
            sess["usuario_perfil"] = "funcionario"
            sess["usuario_nome"] = "Funcionario Teste"

    # =========================================================================
    # 1. US #6 — Movimentacoes de pedidos (Criar, Editar, Cancelar)
    # =========================================================================

    def test_criar_pedido_registra_saida_com_todos_os_detalhes(self):
        """Criar pedido registra saida; confere material, quantidade, usuario e motivo."""
        self.logar_funcionario()
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
            pedido = Pedido.query.filter_by(cliente_id=self.cliente_id).first()
            self.assertIsNotNone(pedido)
            self.assertEqual(pedido.metros_consumidos, 2.00)

            mov = MovimentacaoEstoque.query.filter_by(
                material_id=self.material_id, tipo="saida"
            ).order_by(MovimentacaoEstoque.id.desc()).first()

            self.assertIsNotNone(mov)
            self.assertEqual(mov.tipo, "saida")
            self.assertEqual(mov.material_id, self.material_id)
            self.assertEqual(mov.quantidade_metros, 2.00)
            self.assertEqual(mov.usuario_id, self.func_id)
            self.assertEqual(mov.motivo, f"Consumo do pedido #{pedido.id}")

    def test_editar_pedido_registra_estorno_e_novo_consumo(self):
        """Editar pedido registra estorno (entrada) e novo consumo (saida); confere detalhes."""
        # Cria pedido inicial consumindo 2.00m
        self.logar_funcionario()
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
            pedido = Pedido.query.filter_by(cliente_id=self.cliente_id).first()
            pedido_id = pedido.id

        # Edita o pedido alterando quantidade para 3 (consumindo 3.00m)
        response = self.client.post(
            f"/pedidos/{pedido_id}/editar",
            data={
                "cliente_id": str(self.cliente_id),
                "categoria": "Lona",
                "tipo": "Lona Branca Brilho",
                "largura": "1.00",
                "altura": "2.00",
                "unidade": "m",
                "quantidade": "3",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            movimentacoes = MovimentacaoEstoque.query.filter_by(
                material_id=self.material_id
            ).order_by(MovimentacaoEstoque.id.asc()).all()

            # Localiza a entrada de estorno e a nova saida
            estorno = next(
                (m for m in movimentacoes if m.tipo == "entrada" and f"Estorno para edição do pedido #{pedido_id}" in m.motivo),
                None,
            )
            novo_consumo = next(
                (m for m in reversed(movimentacoes) if m.tipo == "saida" and f"Consumo do pedido #{pedido_id}" in m.motivo),
                None,
            )

            self.assertIsNotNone(estorno, "Estorno deve ser registrado na edicao do pedido")
            self.assertEqual(estorno.quantidade_metros, 2.00)
            self.assertEqual(estorno.usuario_id, self.func_id)
            self.assertEqual(estorno.motivo, f"Estorno para edição do pedido #{pedido_id}")

            self.assertIsNotNone(novo_consumo, "Novo consumo deve ser registrado na edicao do pedido")
            self.assertEqual(novo_consumo.quantidade_metros, 3.00)
            self.assertEqual(novo_consumo.usuario_id, self.func_id)
            self.assertEqual(novo_consumo.motivo, f"Consumo do pedido #{pedido_id}")

    def test_cancelar_pedido_registra_devolucao(self):
        """Cancelar pedido registra devolucao (entrada); confere material, quantidade, usuario e motivo."""
        self.logar_funcionario()
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
            pedido = Pedido.query.filter_by(cliente_id=self.cliente_id).first()
            pedido_id = pedido.id

        # Cancela o pedido
        response = self.client.post(f"/pedidos/{pedido_id}/cancelar", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            # Pedido foi excluido
            self.assertIsNone(Pedido.query.get(pedido_id))

            # Movimentacao de devolucao registrada
            devolucao = MovimentacaoEstoque.query.filter_by(
                material_id=self.material_id, tipo="entrada"
            ).order_by(MovimentacaoEstoque.id.desc()).first()

            self.assertIsNotNone(devolucao)
            self.assertEqual(devolucao.quantidade_metros, 2.00)
            self.assertEqual(devolucao.material_id, self.material_id)
            self.assertEqual(devolucao.usuario_id, self.func_id)
            self.assertEqual(devolucao.motivo, f"Estorno por cancelamento do pedido #{pedido_id}")

    # =========================================================================
    # 2. Alteracoes manuais no estoque
    # =========================================================================

    def test_cadastro_material_registra_entrada_no_historico(self):
        """Cadastro de novo material registra entrada com bobinas e metragem inicial."""
        self.logar_admin()
        response = self.client.post(
            "/estoque/novo",
            data={
                "categoria": "Adesivo",
                "nome": "Vinil Jateado Teste",
                "codigo_barras": "7891112223334",
                "largura_m": "1.22",
                "unidades": "2",
                "estoque_minimo": "10.0",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            mat = Material.query.filter_by(codigo_barras="7891112223334").first()
            self.assertIsNotNone(mat)

            mov = MovimentacaoEstoque.query.filter_by(material_id=mat.id).first()
            self.assertIsNotNone(mov)
            self.assertEqual(mov.tipo, "entrada")
            self.assertEqual(mov.quantidade_bobinas, 2)
            self.assertEqual(mov.quantidade_metros, 100.0)
            self.assertEqual(mov.usuario_id, self.admin_id)
            self.assertEqual(mov.motivo, "Estoque inicial no cadastro do material")

    def test_adicao_manual_de_bobina_registra_entrada(self):
        """Adicao manual de bobina registra entrada de 1 unidade e 50 metros."""
        self.logar_admin()
        response = self.client.post(
            f"/estoque/material/{self.material_id}/adicionar-unidade",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            mov = MovimentacaoEstoque.query.filter_by(
                material_id=self.material_id, tipo="entrada"
            ).order_by(MovimentacaoEstoque.id.desc()).first()

            self.assertIsNotNone(mov)
            self.assertEqual(mov.quantidade_bobinas, 1)
            self.assertEqual(mov.quantidade_metros, 50.0)
            self.assertEqual(mov.usuario_id, self.admin_id)
            self.assertEqual(mov.motivo, "Adição manual de bobina")

    def test_remocao_manual_de_bobina_registra_saida_da_metragem_removida(self):
        """Remocao manual de bobina registra saida da metragem da bobina removida."""
        self.logar_admin()
        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            metros_antes = mat.metros_disponiveis

        response = self.client.post(
            f"/estoque/material/{self.material_id}/remover-unidade",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            metros_depois = mat.metros_disponiveis
            diferenca = metros_antes - metros_depois

            mov = MovimentacaoEstoque.query.filter_by(
                material_id=self.material_id, tipo="saida"
            ).order_by(MovimentacaoEstoque.id.desc()).first()

            self.assertIsNotNone(mov)
            self.assertEqual(mov.quantidade_bobinas, 1)
            self.assertEqual(mov.quantidade_metros, diferenca)
            self.assertEqual(mov.usuario_id, self.admin_id)
            self.assertEqual(mov.motivo, "Remoção manual de bobina")

    def test_ajuste_manual_registra_diferenca_e_saldo_anterior_posterior(self):
        """Ajuste de metragem registra diferenca e saldo anterior/posterior no motivo."""
        self.logar_admin()
        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            metros_antes = mat.metros_disponiveis  # 100.00m

        novo_saldo = 72.50
        response = self.client.post(
            f"/estoque/material/{self.material_id}/editar-metros",
            data={"metros_disponiveis": str(novo_saldo)},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            self.assertEqual(mat.metros_disponiveis, novo_saldo)

            mov = MovimentacaoEstoque.query.filter_by(
                material_id=self.material_id, tipo="ajuste"
            ).order_by(MovimentacaoEstoque.id.desc()).first()

            self.assertIsNotNone(mov)
            diferenca_esperada = round(abs(novo_saldo - metros_antes), 2)
            self.assertEqual(mov.quantidade_metros, diferenca_esperada)
            self.assertEqual(mov.usuario_id, self.admin_id)
            motivo_esperado = f"Ajuste manual: {metros_antes:.2f} m → {novo_saldo:.2f} m"
            self.assertEqual(mov.motivo, motivo_esperado)

    def test_salvar_mesmo_saldo_nao_gera_movimentacao(self):
        """Salvar exatamente o mesmo saldo de metragem nao gera registro de movimentacao."""
        self.logar_admin()
        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            saldo_atual = mat.metros_disponiveis
            total_movimentacoes_antes = MovimentacaoEstoque.query.filter_by(material_id=mat.id).count()

        response = self.client.post(
            f"/estoque/material/{self.material_id}/editar-metros",
            data={"metros_disponiveis": str(saldo_atual)},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            total_movimentacoes_depois = MovimentacaoEstoque.query.filter_by(material_id=self.material_id).count()
            self.assertEqual(
                total_movimentacoes_antes,
                total_movimentacoes_depois,
                "Nao deve gerar movimentacao quando o saldo nao for alterado",
            )

    # =========================================================================
    # 3. Consistencia do historico
    # =========================================================================

    def test_operacao_rejeitada_nao_altera_saldo_nem_historico(self):
        """Operacao rejeitada (quantidade de entrada invalida) nao altera saldo nem cria movimentacao."""
        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            saldo_antes = mat.metros_disponiveis
            total_mov_antes = MovimentacaoEstoque.query.count()

        # Envia quantidade de bobinas invalida (<= 0)
        response = self.client.post(
            "/estoque/entrada",
            data={
                "codigo_barras": "7890000000011",
                "quantidade_bobinas": "-2",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("A quantidade de bobinas deve ser maior que zero".encode("utf-8"), response.data)

        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            self.assertEqual(mat.metros_disponiveis, saldo_antes)
            self.assertEqual(MovimentacaoEstoque.query.count(), total_mov_antes)

    def test_falha_na_gravacao_desfaz_ambos_saldo_e_historico(self):
        """Falha com rollback na transacao desfaz simultaneamente a alteracao de saldo e o historico."""
        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            saldo_original = mat.metros_disponiveis
            total_mov_original = MovimentacaoEstoque.query.filter_by(material_id=mat.id).count()

            # Executa operacao e forca rollback
            mat.bobinas.append(BobinaEstoque(metros_restantes=50.0))
            registrar_movimentacao(
                mat, "entrada", 50.0, self.admin_id, "Movimentacao temporaria com falha"
            )
            # Simula falha e desfaz com rollback
            db.session.rollback()

            mat_recarregado = Material.query.get(self.material_id)
            self.assertEqual(mat_recarregado.metros_disponiveis, saldo_original)
            total_mov_depois = MovimentacaoEstoque.query.filter_by(material_id=mat.id).count()
            self.assertEqual(total_mov_original, total_mov_depois)

    def test_material_com_movimentacoes_nao_pode_ser_excluido(self):
        """Material com historico de movimentacoes nao pode ser excluido; saldo e historico preservados."""
        self.logar_admin()
        # Garante que existe pelo menos uma movimentacao associada
        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            registrar_movimentacao(mat, "entrada", 50.0, self.admin_id, "Entrada para teste de exclusao")
            db.session.commit()

        # Tenta excluir o material
        response = self.client.post(
            f"/estoque/material/{self.material_id}/excluir",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Material com histórico de movimentações não pode ser excluído".encode("utf-8"),
            response.data,
        )

        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            self.assertIsNotNone(mat, "Material com movimentacoes nao deve ser excluido")

    def test_filtros_e_ordenacao_do_historico(self):
        """Conferir filtros por tipo e material e ordenacao decrescente no historico."""
        with self.app.app_context():
            mat = Material.query.get(self.material_id)
            outro_mat = Material.query.filter_by(codigo_barras="7890000000028").first()

            mov1 = registrar_movimentacao(mat, "entrada", 50.0, self.admin_id, "Historico 1 Entrada Mat1")
            db.session.commit()
            mov2 = registrar_movimentacao(mat, "saida", 10.0, self.admin_id, "Historico 2 Saida Mat1")
            db.session.commit()
            mov3 = registrar_movimentacao(outro_mat, "entrada", 50.0, self.admin_id, "Historico 3 Entrada Mat2")
            db.session.commit()

            # Ordenacao decrescente
            lista_todas = listar_movimentacoes()
            self.assertEqual(lista_todas[0].id, mov3.id)
            self.assertEqual(lista_todas[1].id, mov2.id)
            self.assertEqual(lista_todas[2].id, mov1.id)

            # Filtro por tipo
            apenas_saidas = listar_movimentacoes(tipo="saida")
            self.assertTrue(all(m.tipo == "saida" for m in apenas_saidas))
            self.assertIn(mov2.id, [m.id for m in apenas_saidas])
            self.assertNotIn(mov1.id, [m.id for m in apenas_saidas])

            # Filtro por material
            apenas_mat1 = listar_movimentacoes(material_id=self.material_id)
            self.assertTrue(all(m.material_id == self.material_id for m in apenas_mat1))
            self.assertIn(mov1.id, [m.id for m in apenas_mat1])
            self.assertIn(mov2.id, [m.id for m in apenas_mat1])
            self.assertNotIn(mov3.id, [m.id for m in apenas_mat1])


if __name__ == "__main__":
    unittest.main()
