from src.web.helpers.handlers import bad_request
from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.web.controllers.auth import login_required
from src.web.forms.users import UserForm
from src.core.auth import create_user, delete_user, update_user
from src.core.auth import list_user, find_user, update_user, paginated_users
from src.core.auth import list_roles, update_user_roles, IntegrytyException


users_blueprint = Blueprint('users', __name__, url_prefix ='/users')
filters = {}


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
    update_args["active"] = form.get("active") == "y" or False

    return update_args

@login_required()
@users_blueprint.get("/")
def index():
    
    params = request.args

    if params.get('active') == 'true':
        filters['active'] = True
    if params.get('active') == 'false':
        filters['active'] = False
    if params.get('active') == 'any':
        filters['active'] = None  

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
    return render_template('users/new.html', form=UserForm(), roles=list_roles())

@login_required()
@users_blueprint.post("/crear")
def create():
    try:
        form = UserForm(request.form)
        if form.validate():
            print("form validated")     
            user = create_user(**parse_from_params(request.form))
            update_user_roles(user, request.form.getlist('roles'))

            flash('El usuario se creó correctamente', 'success')
            return redirect(url_for('users.index'))
    except IntegrytyException:
        flash('El nombre de usuario o email ya existen', 'error')
        return new()
    return new()    


@login_required()
@users_blueprint.get("/<int:id>/editar")
def edit(id):
    item = find_user(id)
    if not item:
        print("item not found")
        return bad_request("User not found")

    form = UserForm(
        firstname   = item.firstname,
        lastname    = item.lastname,
        username    = item.username,
        email       = item.email,
        password    = item.password,
        active      = item.active
    )    
    return render_template('users/edit.html', form=form, id=id, roles=list_roles())

@login_required()
@users_blueprint.post("/update")
def update():
    user_id = request.form['id']
    if not request.form:
        return bad_request("No se ha enviado ningún formulario")
    form = UserForm(request.form)

    try:
        if form.validate():
            update_user(user_id, parse_from_params(request.form))
            update_user_roles(find_user(user_id), request.form.getlist('roles'))

            flash('usuario modificado con éxito', 'success')
            return redirect(url_for('users.index'))
    except IntegrytyException:
        flash('El nombre de usuario o email ya existen', 'error')
        return edit(user_id)
    return edit(user_id)    

@login_required()
@users_blueprint.get("/<int:user_id>/destroy")
def destroy(user_id):
    delete_user(user_id)
    flash("El usuario se eliminó correctamente", 'success')
    return redirect(url_for('users.index'))
