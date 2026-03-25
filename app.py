from flask import Flask
from database.db import db
from models.cliente import Cliente

from controllers.pedido_controller import pedido_bp
from controllers.estoque_controller import estoque_bp
from controllers.cliente_controller import cliente_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# registrar rotas
app.register_blueprint(pedido_bp)
app.register_blueprint(estoque_bp)
app.register_blueprint(cliente_bp)

@app.route("/")
def home():
    return "Sistema rodando!"

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)