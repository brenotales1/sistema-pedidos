"""Modelo de usuario do sistema."""

from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    """Representa um usuario autorizado a acessar o sistema."""

    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(
        db.String(20),
        nullable=False,
        default="funcionario",
    )

    def definir_senha(self, senha):
        """Gera e armazena o hash da senha."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        """Verifica se a senha informada corresponde ao hash."""
        return check_password_hash(self.senha_hash, senha)