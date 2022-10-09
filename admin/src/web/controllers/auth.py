from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import auth


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(function):
    def login_decorator(*args):
        if session.get('user') is None:
            flash('Usted debe estar loggeado para acceder a esta página', 'error')
            return redirect(url_for('auth.login'))
        function(*args)

    login_decorator.__name__ = function.__name__
    return login_decorator

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

  session['user'] = params["email"]
  flash('La sesión se inició correctamente', 'success')
  return(redirect(url_for("home")))

@auth_blueprint.get("/logout")
def logout():
  del session['user']
  session.clear()
  flash("La sesión se cerró correctamente", 'success')

  return redirect(url_for("auth.login"))