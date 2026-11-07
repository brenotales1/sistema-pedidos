"""Consulta administrativa das tentativas de notificacao (US #10)."""
from flask import Blueprint, render_template, request
from sqlalchemy.orm import joinedload

from controllers.auth_required import admin_required
from models.notificacao_whatsapp import NotificacaoWhatsApp

notificacao_bp = Blueprint("notificacao", __name__)

STATUS_NOTIFICACAO = {
    "aceito": "Envio aceito pela API",
    "falha": "Falha no envio",
    "pendente": "Resultado pendente de registro",
    "indeterminado": "Resultado indeterminado",
    "status_incompativel": "Nao enviado: status incompativel",
    "desabilitado": "Não enviado: WhatsApp desativado",
    "bloqueado_testing": "Não enviado: ambiente de testes",
    "sem_destinatario": "Não enviado: telefone ausente ou inválido",
    "configuracao_invalida": "Não enviado: configuração inválida",
}


@notificacao_bp.route("/notificacoes")
@admin_required
def historico():
    """Lista tentativas recentes sem alterar registros ou disparar envios."""
    status = request.args.get("status", "").strip()
    if status not in STATUS_NOTIFICACAO:
        status = ""
    consulta = NotificacaoWhatsApp.query.options(
        joinedload(NotificacaoWhatsApp.cliente),
    )
    if status:
        consulta = consulta.filter_by(resultado=status)
    pagina = consulta.order_by(
        NotificacaoWhatsApp.data_hora.desc(), NotificacaoWhatsApp.id.desc(),
    ).paginate(per_page=25, error_out=False)
    return render_template(
        "notificacoes/historico.html", pagina=pagina,
        status=status, status_notificacao=STATUS_NOTIFICACAO,
    )
