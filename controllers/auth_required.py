from functools import wraps

from flask import session, redirect, url_for


def login_required(func):
    """Permite acesso somente a usuarios autenticados."""

    @wraps(func)
    def decorated_function(*args, **kwargs):

        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return decorated_function


def admin_required(func):
    """Permite acesso somente a usuarios administradores."""

    @wraps(func)
    def decorated_function(*args, **kwargs):

        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))

        if session.get("usuario_perfil") != "admin":
            return redirect(url_for("home"))

        return func(*args, **kwargs)

    return decorated_function