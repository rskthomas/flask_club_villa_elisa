from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from functools import wraps

from src.core import auth
from src.core.auth import can_perform
from src.web.helpers.get_header_info import get_header_info


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(argument=None):
    """Decorator to check if user is logged in"""

    @wraps(argument)
    def argument_wrapper(function):
        @wraps(function)
        def login_decorator(*args, **kwargs):
            """Checks if user is logged in and has the required permissions"""

            if session.get("user") is None:
                flash("Primero ingresá para visitar esa página.", "error")
                return redirect(url_for("auth.login"))
            if argument and not can_perform(session.get("user"), argument):
                flash("No tenés permisos suficientes para realizar esa acción.", "error")
                return redirect(url_for("auth.login"))
            return function(*args, **kwargs)

        return login_decorator

    return argument_wrapper


@auth_blueprint.get("/")
def login():
    """If the user is unauthenticated, renders the authentication page. Otherwise redirects to the home page."""

    if session.get("user") is None:
        return render_template("auth/login.html", header_info=get_header_info())
    else:
        flash("Ya ingresaste al sistema.", "success")
        return redirect(url_for("home"))


@auth_blueprint.post("/authenticate")
def authenticate():
    params = request.form
    user = auth.find_user_by_mail_and_pass(params["email"], params["password"])

    if not user:
        flash("El correo electrónico o la clave son incorrectos.", "error")
        return redirect(url_for("auth.login"))

    session["user"] = user.id
    flash("Ingresaste al sistema.", "success")
    return redirect(url_for("home"))


@auth_blueprint.get("/logout")
def logout():
    del session["user"]
    session.clear()
    flash("Saliste del sistema.", "success")

    return redirect(url_for("auth.login"))
