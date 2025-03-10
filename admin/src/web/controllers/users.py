import io
import csv
from flask import Blueprint, render_template, request, flash
from flask import redirect, url_for, make_response
from src.web.helpers.handlers import bad_request
from src.web.controllers.auth import login_required
from src.web.forms.users import UserForm, EditUserForm
from src.core.auth import create_user, delete_user, update_user
from src.core.auth import list_user, find_user, update_user, paginated_users
from src.core.auth import list_roles, update_user_roles, IntegrytyException
from src.web.helpers.get_header_info import get_header_info


users_blueprint = Blueprint("users", __name__, url_prefix="/users")


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
    update_args["password"] = form.get("password") or form.get("edit_password")
    update_args["active"] = form.get("active") == "y" or False

    return update_args


def current_page(request):
    return int(request.args.get("page", 1))


def parse_filters(request):
    filters = {}
    params = request.args
    if params.get("active", "").lower() == "true":
        filters["active"] = True
    if params.get("active", "").lower() == "false":
        filters["active"] = False
    if params.get("active") == "any":
        filters["active"] = None

    filters["email"] = params.get("email")

    return filters


def csv_ready_user(user):
    """Format Sql alchemy user record into a
        csv-ready dictionaty
    Args:
        User: record mapped from DB

    Returns:
        dict: csv-ready dict
    """ """Convers a user into a"""
    return {
        "id": user.id,
        "Nombre": user.firstname,
        "Apellido": user.lastname,
        "Nombre de usuario": user.username,
        "email": user.email,
        "Activo": "Si" if user.active else "No",
        "Roles": ", ".join(list(map(lambda x: x.name, user.roles))),
        "Fecha de alta": user.created_at,
    }


@users_blueprint.get("/")
@login_required('users_index')
def index():
    """Renders the user index page for the authenticated user."""
    filters = parse_filters(request)
    pagination_data = paginated_users(filters, current_page(request))

    return render_template(
        "users/index.html",
        users=pagination_data["items"],
        filters=filters,
        current_page=current_page(request),
        pages=pagination_data["pages"],
        header_info=get_header_info(),
    )


@users_blueprint.get("/csv_export")
@login_required('users_index')
def csv_export():
    """Download a CSV file with all users that fulfill the current filters selected in the index member grid."""
    users_list = list(map(lambda user: csv_ready_user(user),
                          list_user(parse_filters(request))))

    output = io.StringIO()
    writer = csv.writer(output)
    header = list(users_list[0].keys())

    writer.writerow(header)

    for user in users_list:
        row = list(map(str, user.values()))
        writer.writerow(row)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    response.headers["Content-type"] = "text/csv"
    return response


@users_blueprint.get("/nuevo")
@login_required('users_create')
def new():
    """Renders the user create page for the authenticated user."""
    return render_template(
        "users/new.html",
        form=UserForm(),
        roles=list_roles(),
        header_info=get_header_info(),
    )


@users_blueprint.post("/crear")
@login_required('users_create')
def create():
    """Confirm the creation of user and redirect to users index page."""
    try:
        form = UserForm(request.form)
        if form.validate():
            print("form validated")
            user = create_user(**parse_from_params(request.form))
            update_user_roles(user, request.form.getlist("roles"))

            flash("El usuario se creó correctamente", "success")
            return redirect(url_for("users.index"))
    except IntegrytyException:
        flash("El nombre de usuario o email ya existen", "error")
        return new()
    return new()


@users_blueprint.get("/<int:id>/editar")
@login_required('users_create')
def edit(id):
    """Renders the user edit page for the authenticated user.
    Args:
        id (int): id of the user
    """
    user = find_user(id)
    if not user:
        print("item not found")
        return bad_request("User not found")

    form = EditUserForm(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        password=user.password,
        active=user.active,
    )
    return render_template(
        "users/edit.html",
        form=form,
        id=id,
        roles=list_roles(),
        user=user,
        header_info=get_header_info(),
    )


@users_blueprint.post("/update")
@login_required('users_update')
def update():
    """Confirm the update of the user and redirect to users index page."""
    user_id = request.form["id"]
    if not request.form:
        return bad_request("No se ha enviado ningún formulario")
    form = EditUserForm(request.form)

    try:
        if form.validate():
            update_user(user_id, parse_from_params(request.form))
            update_user_roles(
                find_user(user_id),
                request.form.getlist("roles"))

            flash("usuario modificado con éxito", "success")
            return redirect(url_for("users.index"))
    except IntegrytyException:
        flash("El nombre de usuario o email ya existen", "error")
        return edit(user_id)
    return edit(user_id)


@users_blueprint.get("/<int:user_id>/destroy")
@login_required('users_destroy')
def destroy(user_id):
    """Delete the user with the id sent by parameter and redirect to users index page.
    Args:
        id (int): id of the user
    """
    delete_user(user_id)
    flash("El usuario se eliminó correctamente", "success")
    return redirect(url_for("users.index"))
