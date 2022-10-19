from src.core.discipline import find_discipline, enroll_member
from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import discipline as Discipline
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from src.web.controllers.auth import login_required


discipline_blueprint = Blueprint("disciplines", __name__, url_prefix="/disciplines")


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
    item = Discipline.find_discipline(id)

    if not item:
        print("item not found")
        return bad_request("Discipline not found")

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
    discipline_id = request.form['id']
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


@discipline_blueprint.post("/<int:id>/delete")
@login_required("discipline_rwd")
def delete(id):
    if not Discipline.delete_discipline(id):
        return bad_request("Discipline not found")

    flash("Disciplina eliminada correctamente", "success")
    return redirect(url_for("disciplines.index"))


@discipline_blueprint.get("/<int:id>/delete")
def delete_error(id):
    return bad_request("No se ha enviado ningun formulario")


@discipline_blueprint.get("/<int:id>")
@login_required("discipline_rw")
def show(id):
    item = Discipline.find_discipline(id)
    return render_template("discipline/show.html", discipline=item)


@discipline_blueprint.get("<int:id>/enrollment")
@login_required()
def enrollment_form(id):
    discipline = find_discipline(id)
    return render_template('discipline/enrollment.html', discipline=discipline)

@discipline_blueprint.post("<int:id>/enrollment")
@login_required()
def create_enrollment(id):
    try:
        enroll_member(id, request.form.get('chosen_member_id'))
    except Exception:
        flash('Ocurrió un error al realizar la inscription', 'error')
        return render_template('discipline/enrollment.html', discipline=find_discipline(id))
    flash("el alta se realizó con éxito", 'success')

    return render_template('discipline/show.html', discipline=find_discipline(id))


@discipline_blueprint.get("<int:id>/members")
@login_required()
def discipline_members(id):
    discipline = find_discipline(id)
    return discipline.members


class DisciplineForm(Form):
    """Represents an html form of Discipline model"""

    name = StringField(
        "Nombre", [validators.Length(min=4, max=25), validators.DataRequired()]
    )
    category = StringField(
        "Categoría", [validators.Length(min=4, max=25), validators.DataRequired()]
    )
    coach = StringField(
        "Nombre/s del instructor/es",
        [validators.Length(min=4, max=50), validators.DataRequired()],
    )
    schedule = StringField(
        "Horario", [validators.Length(min=4, max=50), validators.DataRequired()]
    )
    monthly_price = StringField(
        "Precio Mensual", [validators.Length(min=1, max=15), validators.DataRequired()]
    )
    active = BooleanField("Habilitado")
