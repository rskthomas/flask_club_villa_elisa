from src.core.auth import can_perform
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import auth

from functools import wraps


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(argument):
    @wraps(argument)
    def argument_wrapper(function):
        @wraps(function)
        def login_decorator(*args,**kwargs):
            if session.get('user') is None:
                flash('Usted debe estar loggeado para acceder a esta página', 'error')
                return redirect(url_for('auth.login'))
            if not can_perform(session.get('user'), argument):
                flash('Usted no tiene permisos necesarios', 'error')
                return redirect(url_for('auth.login'))
            return function(*args, **kwargs)

        return login_decorator
    return argument_wrapper

@auth_blueprint.get("/")
def login():
  return render_template("auth/login.html")

@auth_blueprint.post("/authenticate")
def authenticate():
  params = request.form
  user = auth.find_user_by_mail_and_pass(params['email'], params['password'])

  if not user:
    flash("Email o clave incorrecta", 'error')
    return(redirect(url_for('auth.login')))

  session['user'] = user.id
  flash('La sesión se inició correctamente', 'success')
  return(redirect(url_for("home")))

@auth_blueprint.get("/logout")
def logout():
  del session['user']
  session.clear()
  flash("La sesión se cerró correctamente", 'success')

  return redirect(url_for("auth.login"))