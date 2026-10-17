"""Funcoes de apoio para calculos e formatacoes de pedidos."""

import unicodedata


def normalizar_busca(valor):
    """Normaliza texto para comparacoes de busca sem acentos e espacos."""
    texto = str(valor or "").strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    return "".join(texto.split())


def converter_para_metros(valor_texto, unidade):
    """Converte um valor informado em metros ou centimetros para metros."""
    valor = float(str(valor_texto).replace(",", "."))
    if unidade == "cm":
        return round(valor / 100, 2)
    return round(valor, 2)


def formatar_metros(valor):
    """Formata um numero decimal como metragem."""
    return f"{valor:.2f}".replace(".", ",") + "m"


def formatar_area(valor):
    """Formata um numero decimal como area em metros quadrados."""
    return f"{valor:.2f}".replace(".", ",") + " m²"


def calcular_melhor_aproveitamento(variacoes, largura_m, altura_m, quantidade, extra_stock=None):
    """Escolhe a variacao de material que gera o menor desperdicio."""
    extra_stock = extra_stock or {}
    area_total = round(largura_m * altura_m * quantidade, 2)
    candidatos = []

    for variacao in variacoes:
        opcoes = []

        if largura_m <= variacao.largura_m:
            opcoes.append(
                {
                    "orientacao": "Padrão",
                    "metros_por_unidade": altura_m,
                    "medida_na_bobina": largura_m,
                }
            )

        if altura_m <= variacao.largura_m:
            opcoes.append(
                {
                    "orientacao": "Rotacionado",
                    "metros_por_unidade": largura_m,
                    "medida_na_bobina": altura_m,
                }
            )

        if not opcoes:
            continue

        melhor_opcao = min(
            opcoes,
            key=lambda opcao: (
                opcao["metros_por_unidade"],
                round(variacao.largura_m - opcao["medida_na_bobina"], 2),
                variacao.largura_m,
            ),
        )

        metros_consumidos = round(melhor_opcao["metros_por_unidade"] * quantidade, 2)
        metros_disponiveis = round(variacao.metros_disponiveis + extra_stock.get(variacao.id, 0), 2)
        metros_restantes_apos_pedido = round(metros_disponiveis - metros_consumidos, 2)
        area_consumida = round(variacao.largura_m * metros_consumidos, 2)
        desperdicio_total = round(area_consumida - area_total, 2)

        if metros_restantes_apos_pedido < 0:
            continue

        candidatos.append(
            {
                "material": variacao,
                "orientacao": melhor_opcao["orientacao"],
                "metros_por_unidade": round(melhor_opcao["metros_por_unidade"], 2),
                "metros_consumidos": metros_consumidos,
                "largura_bobina": round(variacao.largura_m, 2),
                "medida_na_bobina": round(melhor_opcao["medida_na_bobina"], 2),
                "sobra_largura": round(variacao.largura_m - melhor_opcao["medida_na_bobina"], 2),
                "area_consumida": area_consumida,
                "desperdicio_total": desperdicio_total,
                "metros_restantes_apos_pedido": metros_restantes_apos_pedido,
            }
        )

    if not candidatos:
        return None

    return min(
        candidatos,
        key=lambda candidato: (
            candidato["desperdicio_total"],
            candidato["largura_bobina"],
            candidato["metros_consumidos"],
            candidato["sobra_largura"],
        ),
    )


def atualizar_status_com_notificacao(pedido, novo_status, usuario_id=None):
    """Persiste a transicao antes do envio e disputa apenas um update por status."""
    from flask import current_app, session
    from sqlalchemy import update
    from database.db import db
    from models.pedido import Pedido
    from services.whatsapp_service import notificar_pedido_finalizado

    from models.cliente import Cliente
    from models.usuario import Usuario
    from models.historico_status_pedido import HistoricoStatusPedido
    from services.constantes import STATUS_PEDIDO
    from models.notificacao_whatsapp import NotificacaoWhatsApp

    if pedido is None or db.session.get(Pedido, pedido.id) is None:
        raise ValueError("Pedido nao encontrado.")
    if novo_status not in STATUS_PEDIDO:
        raise ValueError("Status do pedido invalido.")
    if not pedido.cliente_id or db.session.get(Cliente, pedido.cliente_id) is None:
        raise ValueError("Vincule um cliente valido ao pedido antes de alterar o status.")
    if usuario_id is None:
        usuario_id = session.get("usuario_id")
    if not usuario_id or db.session.get(Usuario, usuario_id) is None:
        raise ValueError("Usuario responsavel invalido. Entre novamente no sistema.")

    anterior = pedido.status
    if anterior == novo_status:
        current_app.logger.info("WhatsApp transicao: pedido=%s envio_solicitado=False resultado=status_inalterado", pedido.id)
        return
    try:
        resultado = db.session.execute(
            update(Pedido).where(Pedido.id == pedido.id, Pedido.status == anterior)
            .values(status=novo_status).execution_options(synchronize_session=False)
        )
        if resultado.rowcount == 1:
            historico = HistoricoStatusPedido(
                pedido_id=pedido.id, status_anterior=anterior,
                novo_status=novo_status, usuario_id=usuario_id)
            db.session.add(historico)
            if novo_status == "Finalizado":
                tentativa = NotificacaoWhatsApp(
                    historico_status=historico, pedido_id=pedido.id,
                    cliente_id=pedido.cliente_id, evento="pedido_finalizado")
                db.session.add(tentativa)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    if resultado.rowcount == 1 and novo_status == "Finalizado":
        db.session.refresh(pedido)
        notificacao = notificar_pedido_finalizado(pedido)
        registrar_resultado_notificacao(tentativa, notificacao)
        return notificacao
    current_app.logger.info("WhatsApp transicao: pedido=%s envio_solicitado=False resultado=sem_transicao_para_finalizado", pedido.id)


def registrar_resultado_notificacao(tentativa, resultado):
    """Atualiza a tentativa existente sem armazenar textos ou dados do destinatario."""
    import re
    from flask import current_app
    from database.db import db

    permitidos = {"aceito", "falha", "desabilitado", "bloqueado_testing",
                  "sem_destinatario", "configuracao_invalida", "status_incompativel"}
    status = getattr(resultado, "status", None)
    sid = getattr(resultado, "sid", None)
    codigo = getattr(resultado, "codigo_erro", None)
    try:
        tentativa.resultado = status if isinstance(status, str) and status in permitidos else "indeterminado"
        tentativa.message_sid = sid if isinstance(sid, str) and len(sid) <= 34 else None
        tentativa.codigo_erro = codigo if type(codigo) is int and 0 < codigo < 1000000 else None
        db.session.commit()
    except Exception:
        # O commit da finalizacao ja ocorreu. A tentativa continua pendente;
        # nao reenviar, nem propagar detalhes da falha de persistencia.
        db.session.rollback()
        current_app.logger.warning("WhatsApp: resultado da tentativa nao persistido")
