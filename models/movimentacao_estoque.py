"""Modelo de dados para historico de movimentacoes de estoque."""

from datetime import datetime, timedelta, timezone
from database.db import db

try:
    from zoneinfo import ZoneInfo
    FUSO_BRASILIA = ZoneInfo("America/Sao_Paulo")
except Exception:
    FUSO_BRASILIA = timezone(timedelta(hours=-3))


class MovimentacaoEstoque(db.Model):
    """Representa uma movimentacao de estoque (entrada, saida ou ajuste)."""

    __tablename__ = "movimentacao_estoque"

    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    quantidade_metros = db.Column(db.Float, nullable=False, default=0.0)
    quantidade_bobinas = db.Column(db.Integer, nullable=False, default=0)
    motivo = db.Column(db.String(255), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=True)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    material = db.relationship("Material", backref=db.backref("movimentacoes", lazy="dynamic"))
    usuario = db.relationship("Usuario", backref=db.backref("movimentacoes", lazy="dynamic"))

    @property
    def data_hora_formatada(self):
        """Retorna a data e hora formatada no horario de Brasilia (UTC-3)."""
        if not self.data_hora:
            return ""
        dt = self.data_hora
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(FUSO_BRASILIA).strftime("%d/%m/%Y %H:%M")
