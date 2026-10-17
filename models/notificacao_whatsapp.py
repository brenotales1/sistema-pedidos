"""Registro minimo de uma tentativa por transicao de finalizacao."""
from datetime import datetime, timezone
from database.db import db


class NotificacaoWhatsApp(db.Model):
    __tablename__ = "notificacao_whatsapp"

    id = db.Column(db.Integer, primary_key=True)
    historico_status_id = db.Column(db.Integer,
        db.ForeignKey("historico_status_pedido.id"), nullable=False, unique=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    evento = db.Column(db.String(40), nullable=False, default="pedido_finalizado")
    resultado = db.Column(db.String(30), nullable=False, default="pendente")
    message_sid = db.Column(db.String(34), nullable=True)
    codigo_erro = db.Column(db.Integer, nullable=True)
    # Sem callback real, nunca atribuir entrega confirmada.
    entrega_confirmada = db.Column(db.Boolean, nullable=False, default=False)

    pedido = db.relationship("Pedido")
    cliente = db.relationship("Cliente")
    historico_status = db.relationship("HistoricoStatusPedido")
