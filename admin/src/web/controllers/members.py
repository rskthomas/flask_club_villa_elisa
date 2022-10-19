from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import member
from wtforms import Form, BooleanField, StringField, validators
from wtforms.fields import EmailField
import pdfkit
from requests import Response

path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


member_blueprint = Blueprint("member", __name__, url_prefix="/miembros")
filters = {}

@member_blueprint.get("/")
def index():
    params = request.args
     
    if params.get('membership_state') == 'true':
        filters['membership_state'] = True
    if params.get('membership_state') == 'false':
        filters['membership_state'] = False

    filters['last_name'] = params.get('last_name')

    current_page = int(params.get('page', 1))

    pagination_data = member.paginated_members(filters, current_page)

    return render_template('members/index.html', 
                            members=pagination_data['items'],
                            filters=filters,
                            current_page=current_page,
                            pages=pagination_data['pages'])


@member_blueprint.get("/create")
def create_view():
    return render_template("members/create.html", form=MemberForm())


@member_blueprint.post("/create")
def create_confirm():
    form = MemberForm(request.form)
    if form.validate():
        print("form validated")
        member.create_member(
            first_name          = form.first_name.data,
            last_name           = form.last_name.data,
            personal_id_type    = form.personal_id_type.data,
            personal_id         = form.personal_id.data,
            gender              = form.gender.data,
            address             = form.address.data,
            membership_state    = form.membership_state.data,
            phone_number        = form.phone_number.data,
            email               = form.email.data
        )
        flash("Miembro creado correctamente", "success")
        return redirect(url_for("member.index"))
    return render_template("members/create.html", form=form)


@member_blueprint.get("/<int:id>/update")
def update_view(id):
    item = member.find_member(id)
    if not item:
        print("item not found")
        return bad_request("Member not found")

    form = MemberForm(
        first_name          = item.first_name,
        last_name           = item.last_name,
        personal_id_type    = item.personal_id_type,
        personal_id         = item.personal_id,
        gender              = item.gender,
        address             = item.address,
        membership_state    = item.membership_state,
        phone_number        = item.phone_number,
        email               = item.email
    )    
    return render_template("members/update.html", form=form, id=id)


@member_blueprint.post("/update")
def update_confirm():
    member_id = request.form['id']
    if not request.form:
        return bad_request("No se ha enviado ningún formulario")
    form = MemberForm(request.form)
    if form.validate():
        member.update_member(
            id                  = member_id,
            first_name          = form.first_name.data,
            last_name           = form.last_name.data,
            personal_id_type    = form.personal_id_type.data,
            personal_id         = form.personal_id.data,
            gender              = form.gender.data,
            address             = form.address.data,
            membership_state    = form.membership_state.data,
            phone_number        = form.phone_number.data,
            email               = form.email.data
        )
        flash("Miembro actualizado correctamente", "success")
        return redirect(url_for("member.index"))


@member_blueprint.post("/<int:id>/delete")
def delete(id):
    if not member.delete_member(id):
        return bad_request("Member not found")

    flash("Miembro eliminado correctamente", "success")
    return redirect(url_for("member.index"))


@member_blueprint.get("/<int:id>/delete")
def delete_error(id):
    return bad_request("No se ha enviado ningun formulario")


@member_blueprint.get("/<int:id>")
def show(id):
    item = member.find_member(id)
    return render_template("members/show.html", member=item)


@member_blueprint.route("/<int:id>/download")
def route_download(id):
    item = member.find_member(id)
    
    # Get the HTML output
    out = render_template("members/show.html", member=item)
    
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
    pdf = pdfkit.from_string(out, options=options, configuration=config)
    
    # Download the PDF
    return Response(pdf, mimetype="application/pdf")    


class MemberForm(Form):
    """Represents an html form of Member model"""

    first_name = StringField(
        "Nombre", [validators.Length(min=4, max=50), validators.DataRequired()]
    )
    last_name = StringField(
        "Apellido", [validators.Length(min=4, max=50), validators.DataRequired()]
    )
    personal_id_type = StringField(
        "Tipo Documento",
        [validators.Length(min=1, max=25), validators.DataRequired()],
    )
    personal_id = StringField(
        "Nro. Documento", [validators.Length(min=1, max=25), validators.DataRequired()]
    )
    gender = StringField(
        "Género", [validators.Length(min=1, max=25), validators.DataRequired()]
    )
    address = StringField(
        "Dirección", [validators.Length(min=1, max=255), validators.DataRequired()]
    )
    phone_number = StringField(
        "Teléfono", [validators.Length(min=1, max=25), validators.DataRequired()]
    )
    email = EmailField(
        'Email', [validators.Length(min=1, max=50), validators.DataRequired(), validators.Email()])
 
    membership_state = BooleanField("Activo")