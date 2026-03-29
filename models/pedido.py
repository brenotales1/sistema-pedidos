from datetime import datetime

from database.db import db


class Pedido(db.Model):
    __tablename__ = "pedido"

    id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    material_nome = db.Column(db.String(120), nullable=False)
    largura_pedido_m = db.Column(db.Float, nullable=False)
    altura_pedido_m = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    unidade_medida = db.Column(db.String(10), nullable=False)
    largura_rolo_usada_m = db.Column(db.Float, nullable=False)
    orientacao = db.Column(db.String(30), nullable=False)
    metros_consumidos = db.Column(db.Float, nullable=False)
    area_total_m2 = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Pendente")
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def largura_rolo_formatada(self):
        return f"{self.largura_rolo_usada_m:.2f}".replace(".", ",") + "m"

    @property
    def metros_consumidos_formatados(self):
        return f"{self.metros_consumidos:.2f}".replace(".", ",") + "m"

    @property
    def area_total_formatada(self):
        return f"{self.area_total_m2:.2f}".replace(".", ",") + " m²"
