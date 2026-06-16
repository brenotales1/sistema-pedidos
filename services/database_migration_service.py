"""Rotinas simples de migracao para manter o SQLite compativel."""

from sqlalchemy import inspect, text

from database.db import db

TABELA_BOBINA_ESTOQUE = "bobina_estoque"
COLUNA_LARGURA_BOBINA = "largura_bobina_usada_m"


def aplicar_migracoes():
    """Executa todas as migracoes pendentes do banco local."""
    renomear_tabela_bobinas()
    renomear_coluna_largura_bobina()
    garantir_coluna_empresa_cliente()
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
