"""Regras de negocio para controle de bobinas no estoque."""

from models.bobina_estoque import BobinaEstoque
from services.constantes import METROS_POR_BOBINA


def ordenar_bobinas_por_metragem(material):
    """Retorna as bobinas do material ordenadas pela menor metragem."""
    return sorted(material.bobinas, key=lambda bobina: bobina.metros_restantes)


def ordenar_bobinas_por_cadastro(material):
    """Retorna as bobinas do material na ordem de cadastro."""
    return sorted(material.bobinas, key=lambda bobina: bobina.id or 0)


def bobina_completa(bobina):
    """Verifica se uma bobina esta praticamente cheia."""
    return abs(bobina.metros_restantes - METROS_POR_BOBINA) < 0.01


def adicionar_bobina(material, quantidade=1):
    """Adiciona uma ou mais bobinas completas ao material."""
    for _ in range(max(quantidade, 0)):
        material.bobinas.append(BobinaEstoque(metros_restantes=METROS_POR_BOBINA))


def remover_bobina(material):
    """Remove uma bobina do material, priorizando bobinas completas."""
    if not material.bobinas:
        return False

    bobinas_ordenadas = sorted(
        material.bobinas,
        key=lambda bobina: (not bobina_completa(bobina), bobina.metros_restantes),
    )
    bobina_removida = bobinas_ordenadas[0]
    material.bobinas.remove(bobina_removida)
    return True


def ajustar_metros_disponiveis(material, metros_disponiveis):
    """Redistribui a metragem disponivel entre as bobinas do material."""
    restante = round(max(metros_disponiveis, 0), 2)

    for bobina in ordenar_bobinas_por_cadastro(material):
        metros_bobina = min(METROS_POR_BOBINA, restante)
        bobina.metros_restantes = round(metros_bobina, 2)
        restante = round(restante - metros_bobina, 2)


def devolver_material(material, metros_para_devolver):
    """Devolve metragem ao estoque quando um pedido e alterado ou cancelado."""
    restante = round(metros_para_devolver, 2)

    if restante <= 0:
        return

    for bobina in ordenar_bobinas_por_metragem(material):
        if restante <= 0:
            break

        espaco_disponivel = round(METROS_POR_BOBINA - bobina.metros_restantes, 2)
        if espaco_disponivel <= 0:
            continue

        reposicao = min(espaco_disponivel, restante)
        bobina.metros_restantes = round(bobina.metros_restantes + reposicao, 2)
        restante = round(restante - reposicao, 2)

    while restante > 0:
        reposicao = min(METROS_POR_BOBINA, restante)
        material.bobinas.append(BobinaEstoque(metros_restantes=reposicao))
        restante = round(restante - reposicao, 2)


def consumir_material(material, metros_necessarios):
    """Consome metragem das bobinas do material para atender um pedido."""
    restante = round(metros_necessarios, 2)

    if restante > material.metros_disponiveis:
        return False

    for bobina in ordenar_bobinas_por_metragem(material):
        if restante <= 0:
            break

        consumo = min(bobina.metros_restantes, restante)
        bobina.metros_restantes = round(bobina.metros_restantes - consumo, 2)
        restante = round(restante - consumo, 2)

        if bobina.metros_restantes <= 0:
            material.bobinas.remove(bobina)

    return restante <= 0
