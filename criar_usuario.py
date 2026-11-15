from getpass import getpass

from app import app
from database.db import db
from models.usuario import Usuario


def main():
    email = input("E-mail da conta: ").strip()
    if not email:
        raise SystemExit("Informe um e-mail.")

    with app.app_context():
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario is None:
            nome = input("Nome: ").strip()
            perfil = input("Perfil (admin/funcionario): ").strip()
            if not nome or perfil not in {"admin", "funcionario"}:
                raise SystemExit("Nome ou perfil invalido.")
            usuario = Usuario(nome=nome, email=email, perfil=perfil)
        else:
            if input("Conta existente. Trocar a senha? (s/N): ").strip().lower() != "s":
                return

        senha = getpass("Nova senha (minimo 12 caracteres): ")
        if len(senha) < 12:
            raise SystemExit("Use uma senha com pelo menos 12 caracteres.")
        if senha != getpass("Confirme a senha: "):
            raise SystemExit("As senhas nao coincidem.")
        usuario.definir_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        print("Conta salva com sucesso.")


if __name__ == "__main__":
    main()
