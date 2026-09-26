from app import app
from database.db import db
from models.usuario import Usuario


with app.app_context():

    # Criar administrador
    admin = Usuario.query.filter_by(
        email="admin@sistema.com"
    ).first()

    if not admin:
        admin = Usuario(
            nome="Administrador",
            email="admin@sistema.com",
            perfil="admin"
        )

        admin.definir_senha("123456")

        db.session.add(admin)

        print("Administrador criado.")

    else:
        print("Administrador já existe.")

    # Criar funcionário
    funcionario = Usuario.query.filter_by(
        email="funcionario@sistema.com"
    ).first()

    if not funcionario:
        funcionario = Usuario(
            nome="Funcionário",
            email="funcionario@sistema.com",
            perfil="funcionario"
        )

        funcionario.definir_senha("123456")

        db.session.add(funcionario)

        print("Funcionário criado.")

    else:
        print("Funcionário já existe.")

    db.session.commit()

    print("Processo concluído.")