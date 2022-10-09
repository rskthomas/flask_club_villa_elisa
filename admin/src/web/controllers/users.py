from src.core.auth import update_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.auth import list_user, find_user, list_roles

users_blueprint = Blueprint('users', __name__, url_prefix ='/users')


@users_blueprint.get("/")
def index():
    return render_template('users/index.html', users=list_user())


@users_blueprint.get("/<int:id>/editar")
def edit(id):
    return render_template('users/edit.html',
                            user=find_user(id),
                            roles=list_roles())

@users_blueprint.post("/update")
def update():
    params = request.form
    user_id = params["id"]
    update_args = {}
    update_args["firstname"] = params["firstname"]
    update_args["lastname"] = params["lastname"]
    update_args["email"] = params["email"]
    update_args["username"] = params["username"]
    update_args["password"] = params["password"]
    update_args["active"] = params["active"] == "on"

    update_user(user_id, update_args)

    flash('usuario modificado con éxito', 'success')
    return redirect(url_for('users.index'))
