"""Validacao e migracao de consumos sem alterar saldos historicos."""
import math
from sqlalchemy import text
from database.db import db
from models.consumo_material import ConsumoMaterial
from models.material import Material
from models.pedido import Pedido


def consumos_do_pedido(pedido):
    if pedido.consumos:
        return [(item.material, item.quantidade_metros) for item in pedido.consumos]
    # Pedidos antigos sem vinculo inequivoco continuam consultaveis.
    materiais = Material.query.filter_by(
        categoria=pedido.categoria, nome=pedido.material_nome,
        largura_m=pedido.largura_bobina_usada_m,
    ).all()
    if len(materiais) != 1:
        return []
    return [(materiais[0], pedido.metros_consumidos)]


def planejar_consumos(material_principal, metros_principais, adicionais, extra_stock):
    plano = [(material_principal, metros_principais, True)]
    ids = {material_principal.id}
    if len(adicionais) > 100:
        raise ValueError("Informe no maximo 100 materiais adicionais.")
    for item in adicionais:
        try:
            material = db.session.get(Material, int(item["material_id"]))
            metros = round(float(str(item["metros"]).replace(",", ".")), 2)
        except (ValueError, TypeError, KeyError, OverflowError):
            raise ValueError("Informe material e consumo em metros validos.")
        if material is None or not math.isfinite(metros) or metros <= 0:
            raise ValueError("Informe material existente e consumo positivo em metros.")
        if material.id in ids:
            raise ValueError("Cada material deve aparecer uma unica vez no pedido.")
        ids.add(material.id)
        if metros > round(material.metros_disponiveis + extra_stock.get(material.id, 0), 2):
            raise ValueError("Estoque insuficiente para um dos materiais adicionais.")
        plano.append((material, metros, False))
    return plano


def migrar_consumos_legados():
    """Associa pedidos antigos uma vez; nao baixa ou devolve estoque."""
    db.session.execute(text(
        "CREATE TABLE IF NOT EXISTS schema_migration (nome VARCHAR(120) PRIMARY KEY)"
    ))
    nome = "pedido_consumo_material_v1"
    if db.session.execute(text(
        "SELECT 1 FROM schema_migration WHERE nome = :nome"
    ), {"nome": nome}).scalar():
        return
    for pedido in Pedido.query.all():
        if pedido.consumos:
            continue
        candidatos = consumos_do_pedido(pedido)
        if len(candidatos) == 1:
            material, metros = candidatos[0]
            if math.isfinite(metros) and metros > 0:
                pedido.consumos.append(ConsumoMaterial(
                    material=material, quantidade_metros=metros, principal=True,
                ))
    db.session.execute(text(
        "INSERT INTO schema_migration (nome) VALUES (:nome)"
    ), {"nome": nome})
    db.session.commit()
