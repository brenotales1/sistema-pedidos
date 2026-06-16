"""Modelo de dados para materiais do estoque."""

from database.db import db


class Material(db.Model):
    """Representa uma variacao de material com categoria, nome e largura."""

    __tablename__ = "material"

    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    largura_m = db.Column(db.Float, nullable=False)

    bobinas = db.relationship(
        "BobinaEstoque",
        back_populates="material",
        cascade="all, delete-orphan",
        lazy="select",
    )

    __table_args__ = (
        db.UniqueConstraint("categoria", "nome", "largura_m", name="uq_material_variacao"),
    )

    @property
    def largura_formatada(self):
        """Retorna a largura do material formatada em metros."""
        return f"{self.largura_m:.2f}".replace(".", ",") + "m"

    @property
    def quantidade_bobinas(self):
        """Retorna a quantidade de bobinas cadastradas para o material."""
        return len(self.bobinas)

    @property
    def metros_disponiveis(self):
        """Calcula a metragem total disponivel somando as bobinas."""
        return round(sum(bobina.metros_restantes for bobina in self.bobinas), 2)

    @property
    def metros_disponiveis_formatados(self):
        """Retorna a metragem disponivel formatada em metros."""
        return f"{self.metros_disponiveis:.2f}".replace(".", ",") + "m"
