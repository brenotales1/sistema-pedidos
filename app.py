from flask import Flask
from database.db import db
from models.cliente import Cliente
from controllers.pedido_controller import pedido_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(pedido_bp)

@app.route("/")
def home():
    return "Sistema rodando!"

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)