from models.rolo_estoque import RoloEstoque
from services.material_service import METROS_POR_ROLO


def adicionar_rolo(material, quantidade=1):
    for _ in range(max(quantidade, 0)):
        material.rolos.append(RoloEstoque(metros_restantes=METROS_POR_ROLO))


def remover_rolo(material):
    if not material.rolos:
        return False

    rolos_ordenados = sorted(
        material.rolos,
        key=lambda rolo: (0 if abs(rolo.metros_restantes - METROS_POR_ROLO) < 0.01 else 1, rolo.metros_restantes),
    )
    rolo_removido = rolos_ordenados[0]
    material.rolos.remove(rolo_removido)
    return True


def devolver_material(material, metros_para_devolver):
    restante = round(metros_para_devolver, 2)

    if restante <= 0:
        return

    rolos_ordenados = sorted(material.rolos, key=lambda rolo: rolo.metros_restantes)

    for rolo in rolos_ordenados:
        if restante <= 0:
            break

        espaco_disponivel = round(METROS_POR_ROLO - rolo.metros_restantes, 2)
        if espaco_disponivel <= 0:
            continue

        reposicao = min(espaco_disponivel, restante)
        rolo.metros_restantes = round(rolo.metros_restantes + reposicao, 2)
        restante = round(restante - reposicao, 2)

    while restante > 0:
        reposicao = min(METROS_POR_ROLO, restante)
        material.rolos.append(RoloEstoque(metros_restantes=reposicao))
        restante = round(restante - reposicao, 2)


def consumir_material(material, metros_necessarios):
    restante = round(metros_necessarios, 2)

    if restante > material.metros_disponiveis:
        return False

    rolos_ordenados = sorted(material.rolos, key=lambda rolo: rolo.metros_restantes)

    for rolo in rolos_ordenados:
        if restante <= 0:
            break

        consumo = min(rolo.metros_restantes, restante)
        rolo.metros_restantes = round(rolo.metros_restantes - consumo, 2)
        restante = round(restante - consumo, 2)

        if rolo.metros_restantes <= 0:
            material.rolos.remove(rolo)

    return restante <= 0
