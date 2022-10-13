from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.web.controllers.auth import login_required
from src.core.auth import create_user, delete_user, update_user
from src.core.auth import list_user, find_user, update_user, paginated_users
from src.core.auth import list_roles, update_user_roles


users_blueprint = Blueprint('users', __name__, url_prefix ='/users')


def parse_from_params(form):
    """
        Parse http form received and convert it to a
        User-like dictionary

    Args:
        form (dict): form received through http and parsed by flask

    Returns:
        dict: object ready to create/update users
    """

    update_args = {}

    update_args["firstname"] = form["firstname"]
    update_args["lastname"] = form["lastname"]
    update_args["email"] = form["email"]
    update_args["username"] = form["username"]
    update_args["password"] = form["password"]
    update_args["active"] = form.get("active") == "on" or False

    return update_args

@login_required()
@users_blueprint.get("/")
def index():
    params = request.args
    filters = {}

    if params.get('active') == 'true':
        filters['active'] = True
    if params.get('active') == 'false':
        filters['active'] = False

    filters['email'] = params.get('email')

    current_page = int(params.get('page', 1))

    pagination_data = paginated_users(filters, current_page);

    return render_template('users/index.html', 
                            users=pagination_data['items'],
                            filters=filters,
                            current_page=current_page,
                            pages=pagination_data['pages'])

@login_required()
@users_blueprint.get("/nuevo")
def new():
    return render_template('users/new.html', roles=list_roles())

@login_required()
@users_blueprint.post("/crear")
def create():
    user = create_user(**parse_from_params(request.form))
    update_user_roles(user, request.form.getlist('roles'))

    flash('El usuario se creó correctamente', 'success')
    return redirect(url_for('users.index'))


@login_required()
@users_blueprint.get("/<int:id>/editar")
def edit(id):
    return render_template('users/edit.html',
                            user=find_user(id),
                            roles=list_roles())

@login_required()
@users_blueprint.post("/update")
def update():
    user_id = request.form['id']
    update_user(user_id, parse_from_params(request.form))
    update_user_roles(find_user(user_id), request.form.getlist('roles'))

    flash('usuario modificado con éxito', 'success')
    return redirect(url_for('users.index'))


@login_required()
@users_blueprint.get("/<int:user_id>/destroy")
def destroy(user_id):
    delete_user(user_id)
    flash("El usuario se eliminó correctamente", 'success')
    return redirect(url_for('users.index'))
