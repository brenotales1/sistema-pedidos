"""Ponto de entrada da aplicacao Flask."""

from flask import Flask, redirect, url_for

from database.db import db
from controllers.cliente_controller import cliente_bp
from controllers.estoque_controller import estoque_bp
from controllers.pedido_controller import pedido_bp
from services.database_migration_service import aplicar_migracoes
from services.material_service import seed_materials


def home():
    """Redireciona a pagina inicial para a lista de pedidos."""
    return redirect(url_for("pedido.lista_pedidos"))


def create_app():
    """Cria e configura a aplicacao Flask."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev"

    db.init_app(app)
    registrar_rotas(app)

    with app.app_context():
        preparar_banco()

    return app


def registrar_rotas(app):
    """Registra os blueprints e a rota inicial."""
    app.register_blueprint(pedido_bp)
    app.register_blueprint(estoque_bp)
    app.register_blueprint(cliente_bp)
    app.add_url_rule("/", "home", home)


def preparar_banco():
    """Aplica migracoes, cria tabelas e cadastra dados iniciais."""
    aplicar_migracoes()
    db.create_all()
    seed_materials()


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
