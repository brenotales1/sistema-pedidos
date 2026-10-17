"""Auditoria persistente das alteracoes de status de pedidos."""
from datetime import datetime, timezone
from database.db import db


class HistoricoStatusPedido(db.Model):
    __tablename__ = "historico_status_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    status_anterior = db.Column(db.String(30), nullable=False)
    novo_status = db.Column(db.String(30), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    # SQLite armazena UTC sem offset, seguindo o padrao dos demais modelos.
    data_hora = db.Column(db.DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    pedido = db.relationship("Pedido")
    usuario = db.relationship("Usuario")
