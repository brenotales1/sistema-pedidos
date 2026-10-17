import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, redirect, url_for

from database.db import db
from controllers.cliente_controller import cliente_bp
from controllers.estoque_controller import estoque_bp
from controllers.pedido_controller import pedido_bp
from controllers.auth_controller import auth_bp

from services.database_migration_service import aplicar_migracoes
from services.material_service import seed_materials


def home():
    """Redireciona a pagina inicial para a lista de pedidos."""
    return redirect(url_for("pedido.lista_pedidos"))


def create_app(test_config=None):
    """Cria e configura a aplicacao Flask.

    ``test_config`` permite sobrescrever a configuracao antes da
    inicializacao do SQLAlchemy, garantindo isolamento nos testes.
    """
    load_dotenv(Path(__file__).with_name(".env"), override=False)
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)
    app.config.update(
        META_PHONE_NUMBER_ID=os.getenv("META_PHONE_NUMBER_ID", "").strip(),
        META_ACCESS_TOKEN=os.getenv("META_ACCESS_TOKEN", "").strip(),
        META_TEMPLATE_NAME=os.getenv("META_TEMPLATE_NAME", "").strip(),
        META_TEMPLATE_LANG=os.getenv("META_TEMPLATE_LANG", "pt_BR").strip(),
        META_VERIFY_TOKEN=os.getenv("META_VERIFY_TOKEN", "").strip(),
        WHATSAPP_ENABLED=os.getenv("WHATSAPP_ENABLED", "false").strip().lower() == "true",
    )

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

    @app.route("/webhook/whatsapp", methods=["GET", "POST"])
    def whatsapp_webhook():
        """Endpoint de webhook para a Cloud API da Meta (WhatsApp Business)."""
        from flask import request
        if request.method == "GET":
            mode = request.args.get("hub.mode")
            token = request.args.get("hub.verify_token")
            challenge = request.args.get("hub.challenge")
            verify_token = os.getenv("META_VERIFY_TOKEN", "").strip()

            if mode == "subscribe" and token == verify_token and verify_token != "":
                app.logger.info("Webhook Meta validado com sucesso!")
                return challenge, 200
            app.logger.warning("Tentativa de verificacao de webhook Meta falhou. Token invalido ou nao configurado.")
            return "Forbidden", 403

        if request.method == "POST":
            payload = request.get_json(silent=True)
            app.logger.info("Webhook Meta evento recebido: %s", payload)
            return "EVENT_RECEIVED", 200

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
