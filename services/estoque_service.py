from models.bobina_estoque import BobinaEstoque
from services.material_service import METROS_POR_BOBINA


def adicionar_bobina(material, quantidade=1):
    for _ in range(max(quantidade, 0)):
        material.bobinas.append(BobinaEstoque(metros_restantes=METROS_POR_BOBINA))


def remover_bobina(material):
    if not material.bobinas:
        return False

    bobinas_ordenadas = sorted(
        material.bobinas,
        key=lambda bobina: (
            0 if abs(bobina.metros_restantes - METROS_POR_BOBINA) < 0.01 else 1,
            bobina.metros_restantes,
        ),
    )
    bobina_removida = bobinas_ordenadas[0]
    material.bobinas.remove(bobina_removida)
    return True


def ajustar_metros_disponiveis(material, metros_disponiveis):
    restante = round(max(metros_disponiveis, 0), 2)

    for bobina in sorted(material.bobinas, key=lambda item: item.id):
        metros_bobina = min(METROS_POR_BOBINA, restante)
        bobina.metros_restantes = round(metros_bobina, 2)
        restante = round(restante - metros_bobina, 2)


def devolver_material(material, metros_para_devolver):
    restante = round(metros_para_devolver, 2)

    if restante <= 0:
        return

    bobinas_ordenadas = sorted(material.bobinas, key=lambda bobina: bobina.metros_restantes)

    for bobina in bobinas_ordenadas:
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
    restante = round(metros_necessarios, 2)

    if restante > material.metros_disponiveis:
        return False

    bobinas_ordenadas = sorted(material.bobinas, key=lambda bobina: bobina.metros_restantes)

    for bobina in bobinas_ordenadas:
        if restante <= 0:
            break

        consumo = min(bobina.metros_restantes, restante)
        bobina.metros_restantes = round(bobina.metros_restantes - consumo, 2)
        restante = round(restante - consumo, 2)

        if bobina.metros_restantes <= 0:
            material.bobinas.remove(bobina)

    return restante <= 0
