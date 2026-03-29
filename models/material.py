from database.db import db


class Material(db.Model):
    __tablename__ = "material"

    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    largura_m = db.Column(db.Float, nullable=False)

    rolos = db.relationship(
        "RoloEstoque",
        back_populates="material",
        cascade="all, delete-orphan",
        lazy="select",
    )

    __table_args__ = (
        db.UniqueConstraint("categoria", "nome", "largura_m", name="uq_material_variacao"),
    )

    @property
    def largura_formatada(self):
        return f"{self.largura_m:.2f}".replace(".", ",") + "m"

    @property
    def quantidade_rolos(self):
        return len(self.rolos)

    @property
    def metros_disponiveis(self):
        return round(sum(rolo.metros_restantes for rolo in self.rolos), 2)

    @property
    def metros_disponiveis_formatados(self):
        return f"{self.metros_disponiveis:.2f}".replace(".", ",") + "m"
