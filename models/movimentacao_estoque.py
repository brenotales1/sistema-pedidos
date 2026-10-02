"""Modelo de dados para historico de movimentacoes de estoque."""

from datetime import datetime
from database.db import db


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
        """Retorna a data e hora formatada em padrao brasileiro."""
        return self.data_hora.strftime("%d/%m/%Y %H:%M")
