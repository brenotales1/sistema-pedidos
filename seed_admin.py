"""Script de seed para criar o primeiro usuario em producao.

Uso (Render - plano gratuito):
  1. Adicione as variaveis de ambiente no painel do Render:
       SEED_EMAIL, SEED_NOME, SEED_PERFIL (admin/funcionario), SEED_SENHA
  2. Mude o Start Command para: python seed_admin.py
  3. Apos o deploy criar o usuario, restaure o Start Command original:
       gunicorn "app:create_app()"
  4. REMOVA as variaveis SEED_* do painel imediatamente.
"""

import os
import sys

from app import app
from database.db import db
from models.usuario import Usuario


def main():
    email = os.environ.get("SEED_EMAIL", "").strip()
    nome = os.environ.get("SEED_NOME", "").strip()
    perfil = os.environ.get("SEED_PERFIL", "admin").strip()
    senha = os.environ.get("SEED_SENHA", "").strip()

    erros = []
    if not email:
        erros.append("SEED_EMAIL nao definido.")
    if not nome:
        erros.append("SEED_NOME nao definido.")
    if not senha:
        erros.append("SEED_SENHA nao definida.")
    if len(senha) < 12:
        erros.append("SEED_SENHA precisa ter pelo menos 12 caracteres.")
    if perfil not in {"admin", "funcionario"}:
        erros.append("SEED_PERFIL deve ser 'admin' ou 'funcionario'.")

    if erros:
        for e in erros:
            print(f"[ERRO] {e}", file=sys.stderr)
        sys.exit(1)

    with app.app_context():
        if Usuario.query.filter_by(email=email).first():
            print(f"[AVISO] Usuario {email} ja existe. Nenhuma alteracao feita.")
            sys.exit(0)

        u = Usuario(nome=nome, email=email, perfil=perfil)
        u.definir_senha(senha)
        db.session.add(u)
        db.session.commit()
        print(f"[OK] Usuario '{nome}' ({email}) com perfil '{perfil}' criado com sucesso.")


if __name__ == "__main__":
    main()
