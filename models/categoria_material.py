from database.db import db


class CategoriaMaterial(db.Model):
    __tablename__ = "categoria_material"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
