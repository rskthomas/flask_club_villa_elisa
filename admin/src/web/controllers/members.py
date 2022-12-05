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
import base64
from src.web.controllers.cdn import file, generate_qr_code

member_blueprint = Blueprint("member", __name__, url_prefix="/miembros")
filters = {}

#this is a simple bugfix for the issue on production that the default profile photo was not being displayed
_DEFAULT_PROFILE_PIC = "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"


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
        profile_photo=profile_photo.strip()
    )

@member_blueprint.get("/<int:id>/carnet/pdf")
@login_required('member_show')
def download_license_pdf(id):
    """Shows users' license based on the receiver id"""

    license_member = member.find_member(id)
    if license_member.profile_photo_name:
        profile_photo = license_member.profile_photo_name.strip()
        file = open(os.path.join(current_app.config['UPLOAD_FOLDER'], profile_photo), 'rb')
        profile_string = base64.b64encode(file.read()).decode('utf-8')
        file.close()
    else:
        profile_string = _DEFAULT_PROFILE_PIC

    #get QRCODE
    qr_buff=generate_qr_code(license_member.id)
    qr_image = base64.b64encode(qr_buff.getvalue())

    # Get the HTML output
    out = render_template(
        "members/license_pdf.html",
        member=license_member,
        profile_photo=profile_string,
        qr_code = qr_image.decode('utf-8')
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
    response = Response(pdf, mimetype = 'application/pdf', headers = {"Content-Disposition":"attachment;filename=license.pdf"})

    return response
    