"""Servico de envio de notificacoes via Meta WhatsApp Cloud API."""
import logging
import os
import re
from dataclasses import dataclass
from flask import current_app
import phonenumbers
import requests


@dataclass(frozen=True)
class ResultadoEnvio:
    status: str
    sid: str | None = None
    codigo_erro: int | None = None


def normalizar_telefone(valor):
    """Aceita numeros nacionais BR ou internacionais com + e valida E.164."""
    if not isinstance(valor, str) or not re.fullmatch(r"[+0-9(). \-]+", valor.strip()):
        return None
    try:
        numero = phonenumbers.parse(valor.strip(), "BR")
    except phonenumbers.NumberParseException:
        return None
    if not phonenumbers.is_valid_number(numero):
        return None
    return "whatsapp:" + phonenumbers.format_number(numero, phonenumbers.PhoneNumberFormat.E164)


def registrar_resultado(pedido, resultado, solicitado):
    """Loga o status sanitizado do envio sem expor dados pessoais ou credenciais."""
    nivel = logging.WARNING if resultado.status in {"falha", "configuracao_invalida"} else logging.INFO
    current_app.logger.log(
        nivel,
        "WhatsApp resultado: pedido=%s envio_solicitado=%s resultado=%s msg_id=%s codigo_erro=%s",
        getattr(pedido, "id", None), solicitado, resultado.status, resultado.sid, resultado.codigo_erro,
    )
    return resultado


def notificar_pedido_finalizado(pedido):
    """Dispara notificacao de finalizacao de pedido via Meta WhatsApp Cloud API."""
    solicitado = False

    def concluir(status, sid=None, codigo_erro=None):
        return registrar_resultado(pedido, ResultadoEnvio(status, sid, codigo_erro), solicitado)

    current_app.logger.info("WhatsApp avaliacao: pedido=%s", getattr(pedido, "id", None))

    if current_app.testing:
        return concluir("bloqueado_testing")

    if current_app.config.get("WHATSAPP_ENABLED") is not True:
        return concluir("desabilitado")

    if pedido.status != "Finalizado":
        return concluir("status_incompativel")

    try:
        cliente = pedido.cliente if pedido.cliente_id else None
        destinatario = normalizar_telefone(cliente.telefone) if cliente else None
        if not destinatario:
            current_app.logger.info("WhatsApp ignorado: pedido=%s motivo=cliente_ou_telefone_invalido", pedido.id)
            return concluir("sem_destinatario")

        meta_token = os.getenv("META_ACCESS_TOKEN", "").strip()
        meta_phone_id = os.getenv("META_PHONE_NUMBER_ID", "").strip()

        if not (meta_token and meta_phone_id):
            current_app.logger.warning("WhatsApp ignorado: pedido=%s motivo=configuracao_incompleta_meta", pedido.id)
            return concluir("configuracao_invalida")

        numero_limpo = destinatario.replace("whatsapp:", "").replace("+", "").strip()
        url_meta = f"https://graph.facebook.com/v21.0/{meta_phone_id}/messages"
        headers_meta = {
            "Authorization": f"Bearer {meta_token}",
            "Content-Type": "application/json"
        }

        meta_template = os.getenv("META_TEMPLATE_NAME", "").strip()
        if meta_template:
            template_data = {
                "name": meta_template,
                "language": {"code": os.getenv("META_TEMPLATE_LANG", "pt_BR")}
            }
            if meta_template != "hello_world":
                template_data["components"] = [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": str(cliente.nome)},
                            {"type": "text", "text": str(pedido.id)}
                        ]
                    }
                ]
            payload_meta = {
                "messaging_product": "whatsapp",
                "to": numero_limpo,
                "type": "template",
                "template": template_data
            }
        else:
            mensagem_texto = f"Olá, {cliente.nome}! Seu pedido #{pedido.id} foi finalizado e está pronto."
            payload_meta = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": numero_limpo,
                "type": "text",
                "text": {"preview_url": False, "body": mensagem_texto}
            }

        solicitado = True
        current_app.logger.info("WhatsApp Meta solicitacao: pedido=%s destino=%s", pedido.id, numero_limpo)
        resp = requests.post(url_meta, json=payload_meta, headers=headers_meta, timeout=10)

        if resp.status_code in (200, 201):
            dados = resp.json()
            msg_id = None
            if "messages" in dados and len(dados["messages"]) > 0:
                msg_id = dados["messages"][0].get("id")
            current_app.logger.info("WhatsApp aceito pela Meta: pedido=%s msg_id=%s", pedido.id, msg_id)
            # Normaliza o identificador gerado pela Meta (wamid.XXX)
            sid_limpo = re.sub(r"[^0-9a-zA-Z]", "", msg_id or "") if msg_id else ""
            sid_formatado = sid_limpo[:34] if sid_limpo else None
            return concluir("aceito", sid=sid_formatado)
        else:
            current_app.logger.warning("Falha WhatsApp Meta: pedido=%s status_http=%s resposta=%s", pedido.id, resp.status_code, resp.text)
            return concluir("falha", codigo_erro=resp.status_code)

    except Exception:
        current_app.logger.warning("Falha WhatsApp Meta: pedido=%s motivo=erro_no_envio", getattr(pedido, "id", None))
        return concluir("falha")
