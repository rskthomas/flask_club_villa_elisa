from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import member
from wtforms import Form, BooleanField, StringField, validators


member_blueprint = Blueprint("member", __name__, url_prefix="/miembros")


@member_blueprint.get("/")
def index():
  members = member.list_members()
  return render_template('members/index.html', members=members)


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
        email               = item.email,
        activation_date     = item.activation_date
    )
    return render_template("members/update.html", form=form, id=id)


@member_blueprint.post("/<int:id>/update")
def update_confirm(id):
    if not request.form:
        return bad_request("No se ha enviado ningún formulario")
    form = MemberForm(request.form)
    if form.validate():
        member.update_member(
            id                  = id,
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
        [validators.Length(min=1, max=3), validators.DataRequired()],
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
    email = StringField(
        "Email", [validators.Length(min=1, max=50), validators.DataRequired()]
    )
    membership_state = BooleanField("Activo")