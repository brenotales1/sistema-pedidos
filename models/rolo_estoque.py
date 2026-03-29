from database.db import db


class RoloEstoque(db.Model):
    __tablename__ = "rolo_estoque"

    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"), nullable=False)
    metros_restantes = db.Column(db.Float, nullable=False, default=50.0)

    material = db.relationship("Material", back_populates="rolos")
