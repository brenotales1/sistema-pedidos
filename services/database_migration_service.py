from sqlalchemy import inspect, text

from database.db import db

TABELA_BOBINA_ESTOQUE = "bobina_estoque"
COLUNA_LARGURA_BOBINA = "largura_bobina_usada_m"


def aplicar_migracoes():
    renomear_tabela_bobinas()
    renomear_coluna_largura_bobina()
    garantir_coluna_empresa_cliente()
    db.session.commit()


def renomear_tabela_bobinas():
    if TABELA_BOBINA_ESTOQUE in listar_tabelas():
        return

    tabela_atual = encontrar_tabela_de_bobinas()
    if tabela_atual:
        executar_sql(
            f"ALTER TABLE {identificador(tabela_atual)} "
            f"RENAME TO {identificador(TABELA_BOBINA_ESTOQUE)}"
        )


def renomear_coluna_largura_bobina():
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
    if "cliente" not in listar_tabelas():
        return

    if "empresa" not in listar_colunas("cliente"):
        executar_sql('ALTER TABLE cliente ADD COLUMN "empresa" VARCHAR(120)')


def encontrar_tabela_de_bobinas():
    for tabela in listar_tabelas():
        if tabela.startswith("sqlite_"):
            continue

        colunas = set(listar_colunas(tabela))
        if {"id", "material_id", "metros_restantes"}.issubset(colunas):
            return tabela

    return None


def encontrar_coluna_largura_bobina(colunas):
    for coluna in colunas:
        if coluna.startswith("largura_") and coluna.endswith("_usada_m"):
            return coluna

    return None


def listar_tabelas():
    return set(inspect(db.engine).get_table_names())


def listar_colunas(tabela):
    return [coluna["name"] for coluna in inspect(db.engine).get_columns(tabela)]


def executar_sql(sql):
    db.session.execute(text(sql))


def identificador(nome):
    return '"' + nome.replace('"', '""') + '"'
