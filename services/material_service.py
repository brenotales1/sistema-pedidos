from database.db import db
from models.material import Material
from models.rolo_estoque import RoloEstoque

METROS_POR_ROLO = 50.0

MATERIAIS_PADRAO = [
    {"categoria": "Adesivo", "nome": "Adesivo Branco Brilho", "largura_m": 1.06},
    {"categoria": "Adesivo", "nome": "Adesivo Branco Brilho", "largura_m": 1.27},
    {"categoria": "Adesivo", "nome": "Adesivo Blackout", "largura_m": 1.06},
    {"categoria": "Adesivo", "nome": "Adesivo Blackout", "largura_m": 1.27},
    {"categoria": "Adesivo", "nome": "Adesivo Transparente", "largura_m": 1.06},
    {"categoria": "Adesivo", "nome": "Adesivo Transparente", "largura_m": 1.27},
    {"categoria": "Lona", "nome": "Lona Branca Brilho", "largura_m": 0.80},
    {"categoria": "Lona", "nome": "Lona Branca Brilho", "largura_m": 1.10},
    {"categoria": "Lona", "nome": "Lona Branca Brilho", "largura_m": 1.40},
    {"categoria": "Lona", "nome": "Lona Branca Brilho", "largura_m": 1.60},
    {"categoria": "Lona", "nome": "Lona Branca Brilho", "largura_m": 1.80},
    {"categoria": "Lona", "nome": "Lona Branca Brilho", "largura_m": 2.20},
    {"categoria": "Lona", "nome": "Lona Branca Brilho", "largura_m": 3.20},
    {"categoria": "Lona", "nome": "Lona Translúcida", "largura_m": 1.10},
    {"categoria": "Lona", "nome": "Lona Translúcida", "largura_m": 1.40},
    {"categoria": "Lona", "nome": "Lona Translúcida", "largura_m": 2.20},
    {"categoria": "Lona", "nome": "Lona Translúcida", "largura_m": 3.20},
    {"categoria": "Tecido", "nome": "Tecido convencional", "largura_m": 1.50},
]


def seed_materials():
    materiais_existentes = {
        (material.categoria, material.nome, round(material.largura_m, 2))
        for material in Material.query.all()
    }

    novos_materiais = []

    for item in MATERIAIS_PADRAO:
        chave = (item["categoria"], item["nome"], round(item["largura_m"], 2))
        if chave in materiais_existentes:
            continue

        novos_materiais.append(Material(**item))
        materiais_existentes.add(chave)

    if novos_materiais:
        db.session.add_all(novos_materiais)
        db.session.commit()

    materiais = Material.query.all()
    novos_rolos = []

    for material in materiais:
        if material.rolos:
            continue

        novos_rolos.append(RoloEstoque(material_id=material.id, metros_restantes=METROS_POR_ROLO))

    if novos_rolos:
        db.session.add_all(novos_rolos)
        db.session.commit()
