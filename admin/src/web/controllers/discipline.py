from src.core.discipline import DisciplineNotFound, MemberNotFound
from flask import Blueprint
from flask import render_template, abort
from flask import request, flash, redirect, url_for, make_response
from flask import session
from src.web.forms.discipline import DisciplineForm
from src.core.discipline import enroll_member, cancel_enrollment
from src.core.discipline import find_discipline, delete_discipline
from src.core.discipline import InactiveDiscipline, InactiveMember
from src.web.helpers.handlers import bad_request
from src.core import discipline as Discipline
from src.web.controllers.auth import login_required
import pdfkit


discipline_blueprint = Blueprint(
    "disciplines",
    __name__,
    url_prefix="/disciplines")


@discipline_blueprint.get("/")
@login_required("discipline_rw")
def index():
    disciplines = Discipline.get_disciplines()
    return render_template("discipline/index.html", disciplines=disciplines)


@discipline_blueprint.get("/create")
@login_required("discipline_rw")
def create():
    return render_template("discipline/create.html", form=DisciplineForm())


@discipline_blueprint.post("/create")
@login_required("discipline_rw")
def create_post():
    form = DisciplineForm(request.form)
    if form.validate():
        print("form validated")
        Discipline.create_discipline(
            name=form.name.data,
            category=form.category.data,
            coach=form.coach.data,
            schedule=form.schedule.data,
            monthly_price=form.monthly_price.data,
            active=form.active.data,
        )
        flash("Disciplina creada correctamente", "success")
        return redirect(url_for("disciplines.index"))

    return render_template("discipline/create.html", form=form)


@discipline_blueprint.get("/<int:id>/update")
@login_required("discipline_rw")
def update(id):
    item = load_discipline(id)

    form = DisciplineForm(
        name=item.name,
        category=item.category,
        coach=item.coach,
        schedule=item.schedule,
        monthly_price=item.monthly_price,
        active=item.active,
    )
    return render_template("discipline/update.html", form=form, id=id)


@discipline_blueprint.post("/update")
@login_required("discipline_rw")
def update_discipline():
    discipline_id = request.form["id"]
    if not request.form:
        return bad_request("No se ha enviado ningun formulario")
    form = DisciplineForm(request.form)
    if form.validate():
        Discipline.update_discipline(
            id=discipline_id,
            name=form.name.data,
            category=form.category.data,
            coach=form.coach.data,
            schedule=form.schedule.data,
            monthly_price=form.monthly_price.data,
            active=form.active.data,
        )
        flash("Disciplina actualizada correctamente", "success")
        return redirect(url_for("disciplines.index"))


@discipline_blueprint.get("/<int:id>/delete")
@login_required("discipline_rwd")
def delete(id):
    if not delete_discipline(id):
        return bad_request("Discipline not found")

    flash("Disciplina eliminada correctamente", "success")
    return redirect(url_for("disciplines.index"))


@discipline_blueprint.get("/<int:id>/delete")
def delete_error(id):
    return bad_request("No se ha enviado ningun formulario")


@discipline_blueprint.get("/<int:id>")
@login_required("discipline_rw")
def show(id):
    discipline = load_discipline(id)
    return render_template("discipline/show.html", discipline=discipline)


@discipline_blueprint.get("<int:id>/enrollment")
@login_required()
def enrollment_form(id):
    discipline = load_discipline(id)
    return render_template("discipline/enrollment.html", discipline=discipline)


@discipline_blueprint.post("<int:id>/enrollment")
@login_required()
def create_enrollment(id):
    try:
        enroll_member(id, request.form.get("chosen_member_id"))
        flash("el alta se realizó con éxito", "success")
    except InactiveDiscipline:
        flash("la disciplina está inactiva", "error")
        return render_template(
            "discipline/enrollment.html", discipline=find_discipline(id)
        )
    except InactiveMember:
        flash("No se puede inscribir a un socio inactivo", "error")
        return render_template(
            "discipline/enrollment.html", discipline=find_discipline(id)
        )

    return render_template(
        "discipline/show.html",
        discipline=find_discipline(id))


@discipline_blueprint.get("<int:id>/members")
@login_required()
def discipline_members(id):
    discipline = load_discipline(id)
    return discipline.members


@discipline_blueprint.get("<int:id>/members/<int:member_id>/cancel")
@login_required()
def destroy_enrollment(id, member_id):
    try:
        cancel_enrollment(id, member_id)
        flash("La inscripcion del socio ha sido realizada con éxtio", "success")
    except DisciplineNotFound:
        flash("La disciplina no se encontró", "error")
        return redirect(url_for("disciplines.index"))
    except MemberNotFound:
        flash("El socio no se encontró", "error")
        return redirect(url_for("disciplines.index"))

    return redirect(url_for("disciplines.show", id=id))


def load_discipline(id):
    """Looks for a discipline in the DB
        in case it's not found, returns a 404 error

    Args:
        id (_type_): id of the discipline

    Returns:
        sqlAlchemy.model: discipline record
    """
    discipline = find_discipline(id)
    if not discipline:
        abort(404)
    return discipline


@discipline_blueprint.route("/download")
@login_required()
def download():
    disciplines = Discipline.get_disciplines()

    # Get the HTML output
    out = render_template("discipline/export.html", disciplines=disciplines)

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
