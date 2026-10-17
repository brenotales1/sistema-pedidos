"""Rotinas simples de migracao para manter o SQLite compativel."""

from sqlalchemy import inspect, text

from database.db import db

TABELA_BOBINA_ESTOQUE = "bobina_estoque"
COLUNA_LARGURA_BOBINA = "largura_bobina_usada_m"
COLUNA_CODIGO_BARRAS = "codigo_barras"

def aplicar_migracoes():
    """Executa todas as migracoes pendentes do banco local."""
    migrar_cliente_id_pedido()
    renomear_tabela_bobinas()
    renomear_coluna_largura_bobina()
    garantir_coluna_empresa_cliente()
    garantir_coluna_codigo_barras_material()
    garantir_tabela_historico_status_pedido()
    garantir_tabela_notificacao_whatsapp()
    db.session.commit()


def renomear_tabela_bobinas():
    """Renomeia a tabela antiga de bobinas para o nome atual."""
    if TABELA_BOBINA_ESTOQUE in listar_tabelas():
        return

    tabela_atual = encontrar_tabela_de_bobinas()
    if tabela_atual:
        executar_sql(
            f"ALTER TABLE {identificador(tabela_atual)} "
            f"RENAME TO {identificador(TABELA_BOBINA_ESTOQUE)}"
        )


def renomear_coluna_largura_bobina():
    """Garante que a coluna de largura da bobina tenha o nome atual."""
    if "pedido" not in listar_tabelas():
        return

    colunas = listar_colunas("pedido")
    if COLUNA_LARGURA_BOBINA in colunas:
        return

    coluna_atual = encontrar_coluna_largura_bobina(colunas)
    if coluna_atual:
        executar_sql(
            f"ALTER TABLE pedido RENAME COLUMN {identificador(coluna_atual)} "
            f"TO {identificador(COLUNA_LARGURA_BOBINA)}"
        )
        return

    executar_sql(
        f"ALTER TABLE pedido ADD COLUMN {identificador(COLUNA_LARGURA_BOBINA)} "
        "FLOAT NOT NULL DEFAULT 0"
    )


def garantir_coluna_empresa_cliente():
    """Adiciona a coluna empresa na tabela de clientes quando ausente."""
    if "cliente" not in listar_tabelas():
        return

    if "empresa" not in listar_colunas("cliente"):
        executar_sql('ALTER TABLE cliente ADD COLUMN "empresa" VARCHAR(120)')

def garantir_coluna_codigo_barras_material():
    """Adiciona a coluna de codigo de barras na tabela de materiais quando ausente."""
    if "material" not in listar_tabelas():
        return

    if COLUNA_CODIGO_BARRAS not in listar_colunas("material"):
        executar_sql(
            'ALTER TABLE material ADD COLUMN "codigo_barras" VARCHAR(50)'
        )

def encontrar_tabela_de_bobinas():
    """Procura uma tabela antiga com estrutura equivalente a bobinas."""
    for tabela in listar_tabelas():
        if tabela.startswith("sqlite_"):
            continue

        colunas = set(listar_colunas(tabela))
        if {"id", "material_id", "metros_restantes"}.issubset(colunas):
            return tabela

    return None


def encontrar_coluna_largura_bobina(colunas):
    """Procura uma coluna antiga compativel com largura da bobina usada."""
    for coluna in colunas:
        if coluna.startswith("largura_") and coluna.endswith("_usada_m"):
            return coluna

    return None


def listar_tabelas():
    """Lista os nomes das tabelas existentes no banco."""
    return set(inspect(db.engine).get_table_names())


def listar_colunas(tabela):
    """Lista os nomes das colunas de uma tabela."""
    return [coluna["name"] for coluna in inspect(db.engine).get_columns(tabela)]


def executar_sql(sql):
    """Executa um comando SQL bruto dentro da sessao atual."""
    db.session.execute(text(sql))


def identificador(nome):
    """Escapa um identificador SQL para uso em comandos de migracao."""
    return '"' + nome.replace('"', '""') + '"'


def migrar_cliente_id_pedido():
    """Migra o vinculo uma unica vez, com DDL e dados na mesma transacao."""
    with db.engine.connect() as conexao:
        # BEGIN explicito inclui o ALTER TABLE na transacao SQLite e serializa migracoes.
        conexao.exec_driver_sql("BEGIN IMMEDIATE")
        try:
            tabelas = inspect(conexao).get_table_names()
            if "pedido" not in tabelas or "cliente" not in tabelas:
                conexao.rollback()
                return
            conexao.exec_driver_sql(
                "CREATE TABLE IF NOT EXISTS schema_migration "
                "(nome VARCHAR(120) PRIMARY KEY)"
            )
            nome = "pedido_cliente_id_v1"
            aplicada = conexao.execute(text(
                "SELECT 1 FROM schema_migration WHERE nome = :nome"
            ), {"nome": nome}).scalar()
            if aplicada:
                conexao.rollback()
                return
            if "cliente_id" not in {c["name"] for c in inspect(conexao).get_columns("pedido")}:
                conexao.exec_driver_sql(
                    "ALTER TABLE pedido ADD COLUMN cliente_id INTEGER REFERENCES cliente(id)"
                )
            conexao.exec_driver_sql("""
                UPDATE pedido SET cliente_id = (
                    SELECT MIN(c.id) FROM cliente c
                    WHERE c.nome COLLATE BINARY = pedido.cliente_nome COLLATE BINARY
                )
                WHERE cliente_id IS NULL AND (
                    SELECT COUNT(*) FROM cliente c
                    WHERE c.nome COLLATE BINARY = pedido.cliente_nome COLLATE BINARY
                ) = 1
            """)
            conexao.execute(text(
                "INSERT INTO schema_migration (nome) VALUES (:nome)"
            ), {"nome": nome})
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise


def garantir_tabela_historico_status_pedido():
    """Adiciona apenas a tabela de auditoria, preservando os registros existentes."""
    from models.historico_status_pedido import HistoricoStatusPedido
    HistoricoStatusPedido.__table__.create(bind=db.engine, checkfirst=True)


def garantir_tabela_notificacao_whatsapp():
    """Cria apenas a nova tabela; reexecucoes preservam dados existentes."""
    from models.notificacao_whatsapp import NotificacaoWhatsApp
    NotificacaoWhatsApp.__table__.create(bind=db.engine, checkfirst=True)
