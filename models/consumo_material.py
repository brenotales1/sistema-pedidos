"""Associacao N:N entre pedidos e materiais, com consumo em metros."""
from database.db import db


class ConsumoMaterial(db.Model):
    __tablename__ = "consumo_material"
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"), primary_key=True)
    quantidade_metros = db.Column(db.Float, nullable=False)
    principal = db.Column(db.Boolean, nullable=False, default=False)

    pedido = db.relationship("Pedido", back_populates="consumos")
    material = db.relationship("Material", back_populates="consumos")
    __table_args__ = (
        db.CheckConstraint("quantidade_metros > 0", name="ck_consumo_material_positivo"),
    )
