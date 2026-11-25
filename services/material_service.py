"""Regras de negocio para cadastro e padronizacao de materiais."""

import unicodedata

from database.db import db
from models.bobina_estoque import BobinaEstoque
from models.categoria_material import CategoriaMaterial
from models.material import Material
from models.pedido import Pedido
from services.constantes import METROS_POR_BOBINA

MATERIAIS_PADRAO = [
    {
        "categoria": "Adesivo",
        "nome": "Adesivo Branco Brilho",
        "largura_m": 1.27,
        "codigo_barras": "7890000000028",
    },
    {
        "categoria": "Adesivo",
        "nome": "Adesivo Blackout",
        "largura_m": 1.27,
        "codigo_barras": "7890000000035",
    },
    {
        "categoria": "Adesivo",
        "nome": "Adesivo Transparente",
        "largura_m": 1.27,
        "codigo_barras": "7890000000042",
    },
    {
        "categoria": "Lona",
        "nome": "Lona Branca Brilho",
        "largura_m": 3.20,
        "codigo_barras": "7890000000011",
    },
    {
        "categoria": "Lona",
        "nome": "Lona Translúcida",
        "largura_m": 3.20,
        "codigo_barras": "7890000000059",
    },
    {
        "categoria": "Tecido",
        "nome": "Tecido convencional",
        "largura_m": 1.50,
        "codigo_barras": "7890000000066",
    },
]


def normalizar_nome(valor):
    """Normaliza nomes para comparacoes sem acentos e espacos duplicados."""
    texto = " ".join(str(valor or "").strip().lower().split())
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(char for char in texto if not unicodedata.combining(char))


def buscar_material_por_codigo_barras(codigo):
    """Busca um material pelo codigo de barras exato. Retorna None se nao encontrado."""
    if not codigo or not codigo.strip():
        return None

    return Material.query.filter_by(codigo_barras=codigo.strip()).first()


def redefinir_metros_material(material, metros_disponiveis):
    """Recria as bobinas de um material a partir da metragem total."""
    restante = round(max(metros_disponiveis, 0), 2)
    material.bobinas.clear()

    while restante > 0:
        metros_bobina = min(METROS_POR_BOBINA, restante)
        material.bobinas.append(BobinaEstoque(metros_restantes=metros_bobina))
        restante = round(restante - metros_bobina, 2)


def consolidar_materiais_repetidos():
    """Une materiais repetidos preservando estoque e referencias de pedidos."""
    grupos = {}

    for material in Material.query.all():
        chave = (normalizar_nome(material.categoria), normalizar_nome(material.nome), material.largura_m)
        grupos.setdefault(chave, []).append(material)

    for materiais in grupos.values():
        if len(materiais) <= 1:
            continue

        material_principal = max(materiais, key=lambda item: (item.largura_m, item.id))
        metros_disponiveis = sum(material.metros_disponiveis for material in materiais)

        for pedido in Pedido.query.filter_by(
            categoria=material_principal.categoria,
            material_nome=material_principal.nome,
            largura_bobina_usada_m=material_principal.largura_m,
        ).all():
            pedido.largura_bobina_usada_m = material_principal.largura_m

        for material in materiais:
            if material.id == material_principal.id:
                continue

            db.session.delete(material)

        material_principal.categoria = material_principal.categoria.strip()
        material_principal.nome = material_principal.nome.strip()
        redefinir_metros_material(material_principal, metros_disponiveis)

    db.session.commit()


def seed_materials():
    """Cadastra categorias, materiais e bobinas iniciais quando necessario."""
    materiais = Material.query.all()
    categorias_existentes = {categoria.nome for categoria in CategoriaMaterial.query.all()}
    novas_categorias = []

    categorias_iniciais = {item["categoria"] for item in MATERIAIS_PADRAO}
    categorias_iniciais.update(material.categoria for material in materiais)

    for nome_categoria in categorias_iniciais:
        if nome_categoria in categorias_existentes:
            continue

        novas_categorias.append(CategoriaMaterial(nome=nome_categoria))
        categorias_existentes.add(nome_categoria)

    if novas_categorias:
        db.session.add_all(novas_categorias)
        db.session.commit()

    if not materiais:
        # Somente materiais criados neste seed recebem estoque inicial.
        # Ausencia de bobinas em materiais existentes significa saldo zero.
        for dados in MATERIAIS_PADRAO:
            material = Material(**dados)
            material.bobinas.append(BobinaEstoque(metros_restantes=METROS_POR_BOBINA))
            db.session.add(material)
        db.session.commit()

    # Consolidacao de cadastros existentes deve ser uma operacao explicita,
    # nunca um efeito colateral de iniciar a aplicacao.


def obter_relatorio_consumo_agregado_sql():
    """Consulta agregada em SQL com GROUP BY e JOIN de 4 tabelas
    (Cliente, Pedido, ConsumoMaterial e Material) para totalizar o
    consumo em metros por categoria e cliente diretamente pelo banco."""
    from sqlalchemy import func
    from models.cliente import Cliente
    from models.consumo_material import ConsumoMaterial

    return (
        db.session.query(
            Cliente.nome.label("cliente_nome"),
            Material.categoria.label("categoria_material"),
            func.sum(ConsumoMaterial.quantidade_metros).label("total_metros"),
            func.count(func.distinct(Pedido.id)).label("total_pedidos"),
        )
        .join(Pedido, ConsumoMaterial.pedido_id == Pedido.id)
        .join(Material, ConsumoMaterial.material_id == Material.id)
        .join(Cliente, Pedido.cliente_id == Cliente.id)
        .group_by(Cliente.nome, Material.categoria)
        .all()
    )

