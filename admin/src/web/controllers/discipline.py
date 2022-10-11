from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import discipline
from wtforms import Form, BooleanField, StringField, PasswordField, validators


discipline_blueprint = Blueprint("disciplines", __name__, url_prefix="/disciplines")


@discipline_blueprint.get("/")
def index():
    disciplines = discipline.get_disciplines()
    return render_template("discipline/index.html", disciplines=disciplines)


@discipline_blueprint.get("/create")
def create():
    return render_template("discipline/create.html", form=DisciplineForm())


@discipline_blueprint.post("/create")
def create_post():
    form = DisciplineForm(request.form)
    if form.validate():
        print("form validated")
        discipline.create_discipline(
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
def update(id):
    item = discipline.find_discipline(id)

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


@discipline_blueprint.post("/<int:id>/update")
def update_discipline(id):
    if not request.form:
        return bad_request("No se ha enviado ningun formulario")
    form = DisciplineForm(request.form)
    if form.validate():
        discipline.update_discipline(
            id=id,
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
def delete(id):
    # TODO CHECK ROLE
    if not discipline.delete_discipline(id):
        return bad_request("Discipline not found")

    flash("Disciplina eliminada correctamente", "success")
    return redirect(url_for("disciplines.index"))


@discipline_blueprint.get("/<int:id>/delete")
def delete_error(id):
    return bad_request("No se ha enviado ningun formulario")


@discipline_blueprint.get("/<int:id>")
def show(id):
    item = discipline.find_discipline(id)
    return render_template("discipline/show.html", discipline=item)


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
