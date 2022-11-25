import pdfkit
import os.path
import re
from pathlib import Path
from flask import Blueprint, Response
from flask import render_template, current_app,send_from_directory
from flask import request, flash, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from src.web.helpers.handlers import bad_request
from src.core.member import IntegrytyException
from src.web.controllers.auth import login_required
from src.web.forms.member import MemberForm
from src.core import member
from src.web.helpers.get_header_info import get_header_info

member_blueprint = Blueprint("member", __name__, url_prefix="/miembros")
filters = {}


@member_blueprint.get("/")
@login_required('member_index')
def index():
    """Renders the member index page for the authenticated user."""
    params = request.args

    if params.get("membership_state") == "true":
        filters["membership_state"] = True
    if params.get("membership_state") == "false":
        filters["membership_state"] = False
    if params.get("membership_state") == "any":
        filters["membership_state"] = None

    filters["last_name"] = params.get("last_name")

    current_page = int(params.get("page", 1))

    pagination_data = member.paginated_members(filters, current_page)

    return render_template('members/index.html',
                           members=pagination_data['items'],
                           filters=filters,
                           current_page=current_page,
                           pages=pagination_data['pages'],
                           header_info=get_header_info())


@member_blueprint.get("/create")
@login_required('member_create')
def create_view():
    """Renders the member create page for the authenticated user."""
    return render_template(
        "members/create.html",
        form=MemberForm(),
        header_info=get_header_info())


@member_blueprint.post("/create")
@login_required('member_create')
def create_confirm():
    """Confirm the creation member and redirect to member index page."""
    form = MemberForm(request.form)
    try:
        if form.validate():
            print("form validated")
            member.create_member(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                personal_id_type=form.personal_id_type.data,
                personal_id=form.personal_id.data,
                gender=form.gender.data,
                address=form.address.data,
                membership_state=form.membership_state.data,
                phone_number=form.phone_number.data,
                email=form.email.data,
            )
            flash("Miembro creado correctamente", "success")
            return redirect(url_for("member.index"))

    except IntegrytyException:
        flash('Ya existe el email ingresado', 'error')
        return render_template(
            "members/create.html",
            form=form,
            header_info=get_header_info())
    return render_template(
        "members/create.html",
        form=form,
        header_info=get_header_info())


@member_blueprint.get("/<int:id>/update")
@login_required('member_update')
def update_view(id):
    """Renders the member update page for the authenticated user.
    Args:
        id (int): id of the member
    """
    item = member.find_member(id)
    if not item:
        print("item not found")
        return bad_request("Member not found")

    form = MemberForm(
        first_name=item.first_name,
        last_name=item.last_name,
        personal_id_type=item.personal_id_type,
        personal_id=item.personal_id,
        gender=item.gender,
        address=item.address,
        membership_state=item.membership_state,
        phone_number=item.phone_number,
        email=item.email,
    )
    return render_template(
        "members/update.html",
        form=form,
        id=id,
        member=item,
        header_info=get_header_info())


@member_blueprint.post("/update")
@login_required('member_update')
def update_confirm():
    """Confirm the update member and redirect to member index page."""
    member_id = request.form["id"]
    if not request.form:
        return bad_request("No se ha enviado ningún formulario")
    form = MemberForm(request.form)

    try:
        current_app.logger.info('Validando formulario')
        if form.validate():
            current_app.logger.info('Formulario válido')
            if 'profile_photo' in request.files and request.files['profile_photo']:
                current_app.logger.info('se recibe foto de perfil')
                file = request.files['profile_photo']
                file_extension_regex_match = re.search(
                    '.*(\.jpg|\.png|\.jpeg)$',
                     file.filename)
                if file_extension_regex_match is None:
                    raise Exception('formato de archivo inválido')
                filename = secure_filename(f"profile-photo-{member_id}{file_extension_regex_match.group(1)}")
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            member.update_member(
                id=member_id,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                personal_id_type=form.personal_id_type.data,
                personal_id=form.personal_id.data,
                gender=form.gender.data,
                address=form.address.data,
                membership_state=form.membership_state.data,
                phone_number=form.phone_number.data,
                email=form.email.data,
                profile_photo_name=filename
            )
            flash("Miembro actualizado correctamente", "success")
            return redirect(url_for("member.index"))
        else:
            flash(form.errors, "error")
    except IntegrytyException:
        flash("Ya existe el email ingresado", "error")
        return redirect(url_for("member.update_view", id=member_id))
    except Exception as err:
        flash(f"Algo salió mal: {err}","error")
        current_app.logger.info(err)
        return redirect(url_for("member.update_view", id=member_id))
    return redirect(url_for("member.update_view", id=member_id))


@member_blueprint.get("/<int:id>/delete")
@login_required('member_destroy')
def delete(id):
    """Delete the member with the id sent by parameter and redirect to member index page.
    Args:
        id (int): id of the member
    """
    if not member.delete_member(id):
        return bad_request("Member not found")

    flash("Miembro eliminado correctamente", "success")
    return redirect(url_for("member.index"))


@member_blueprint.get("/<int:id>")
@login_required('member_show')
def show(id):
    """Renders the member show page for the authenticated user.
    Args:
        id (int): id of the member
    """
    item = member.find_member(id)
    return render_template(
        "members/show.html",
        member=item,
        header_info=get_header_info())


@member_blueprint.route("/download")
@login_required('member_index')
def route_download():
    """Render a PDF view with all the members that fulfill the current filters selected in the index member grid."""
    params = request.args

    if params.get("membership_state") == "true":
        filters["membership_state"] = True
    if params.get("membership_state") == "false":
        filters["membership_state"] = False

    filters["last_name"] = params.get("last_name")

    current_page = int(params.get("page", 1))

    pagination_data = member.paginated_members(filters, current_page)

    # Get the HTML output
    out = render_template(
        "members/export.html",
        members=pagination_data["items"],
        filters=filters,
        current_page=current_page,
        pages=pagination_data["pages"],
        header_info=get_header_info()
    )

    # PDF options
    options = {
        "orientation": "landscape",
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
    }

    # Build PDF from HTML
    pdf = pdfkit.from_string(out, options=options)

    # Download the PDF
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "filename=output.pdf"
    return response


@member_blueprint.get("/<int:id>/carnet")
@login_required('member_show')
def show_license(id):
    """Shows users' license based on the receiver id"""

    license_member = member.find_member(id)
    if license_member.profile_photo_name:
        profile_photo = license_member.profile_photo_name
    else:
        profile_photo = 'default-profile-photo.jpg'

    # Get the HTML output
    return render_template(
        "members/license.html",
        member=license_member,
        profile_photo=profile_photo
    )

@member_blueprint.get("/<int:id>/carnet/pdf")
@login_required('member_show')
def show_license_idf(id):
    """Shows users' license based on the receiver id"""

    license_member = member.find_member(id)
    if license_member.profile_photo_name:
        profile_photo = license_member.profile_photo_name
    else:
        profile_photo = 'default-profile-photo.jpg'

    # Get the HTML output
    out = render_template(
        "members/license.html",
        member=license_member,
        profile_photo=profile_photo
    )

    # PDF options
    options = {
        "orientation": "landscape",
        "page-size": "A4",
        "encoding": "UTF-8",
        "enable-local-file-access": True
    }

    # Build PDF from HTML
    pdf = pdfkit.from_string(out, options=options, css = './public/style.css')

    # Download the PDF
    response = Response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "filename=output.pdf"
    return response
