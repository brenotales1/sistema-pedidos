import os
from flask import Flask, redirect, url_for

from database.db import db
from controllers.cliente_controller import cliente_bp
from controllers.estoque_controller import estoque_bp
from controllers.pedido_controller import pedido_bp
from controllers.auth_controller import auth_bp

from services.database_migration_service import aplicar_migracoes
from services.material_service import seed_materials


def _carregar_env():
    """Carrega variaveis de ambiente de um arquivo .env local se existir."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.isfile(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#") and "=" in linha:
                    chave, valor = linha.split("=", 1)
                    os.environ.setdefault(chave.strip(), valor.strip().strip("\"'"))


_carregar_env()


def home():
    """Redireciona a pagina inicial para a lista de pedidos."""
    return redirect(url_for("pedido.lista_pedidos"))


def create_app(test_config=None):
    """Cria e configura a aplicacao Flask.

    ``test_config`` permite sobrescrever a configuracao antes da
    inicializacao do SQLAlchemy, garantindo isolamento nos testes.
    """
    app = Flask(__name__)

    database_url = os.environ.get("DATABASE_URL", "sqlite:///database.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    if test_config:
        app.config.update(test_config)

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
    app.register_blueprint(auth_bp)
    app.add_url_rule("/", "home", home)


def preparar_banco():
    """Aplica migracoes, cria tabelas e cadastra dados iniciais."""
    aplicar_migracoes()
    db.create_all()
    seed_materials()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
