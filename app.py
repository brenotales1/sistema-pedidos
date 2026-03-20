from flask import Flask, render_template
from database.db import db
from models.cliente import Cliente

app = Flask(__name__)

# Configuração do banco (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco
db.init_app(app)

# Rota de teste
@app.route("/")
def home():
    return "Sistema rodando!"

@app.route("/pedidos")
def pedidos():
    return render_template("pedidos/lista.html")

# Criar banco automaticamente
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)