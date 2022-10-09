from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import discipline
from wtforms import Form, BooleanField, StringField, PasswordField, validators



discipline_blueprint = Blueprint("disciplines", __name__, url_prefix="/disciplines")


@discipline_blueprint.get("/")
def list():
    disciplines = discipline.get_disciplines()
    return render_template("discipline/index.html", disciplines=disciplines)


@discipline_blueprint.get("/create")
def create():
    return render_template("discipline/create.html")


@discipline_blueprint.post("/create")
def create_post():
    if not request.form:
        bad_request("No se ha enviado ningun formulario")

    name = request.form.get("name")
    category = request.form.get("category")
    coach = request.form.get("coach")
    schedule = request.form.get("schedule")
    monthly_price = request.form.get("monthly_price")
    active = request.form.get("active")
    if active == "":
        active = False
    else:
        active = True

    discipline.create_discipline(
        name=name,
        category=category,
        coach=coach,
        schedule=schedule,
        monthly_price=monthly_price,
        active=active,
    )
    flash("Discipline created")
    return redirect(url_for("disciplines.create"))


@discipline_blueprint.get("/update/<int:id>")
def update(id):
    item = discipline.find_discipline_by_id(id)
    return render_template("discipline/update.html", discipline=item)


@discipline_blueprint.put("/update/<int:id>")
def update_discipline(id):
    if not request.form:
        bad_request("No se ha enviado ningun formulario")
    name = request.form.get("name")
    category = request.form.get("category")
    coach = request.form.get("coach")
    schedule = request.form.get("schedule")
    monthly_price = request.form.get("monthly_price")
    active = request.form.get("active")
    if active == "":
        active = False
    else:
        active = True

    discipline.update_discipline(
        id,
        name=name,
        category=category,
        coach=coach,
        schedule=schedule,
        monthly_price=monthly_price,
        active=active,
    )
    flash("Discipline updated")
    return redirect(url_for("disciplines.update", id=id))


@discipline_blueprint.post("/delete/<int:id>")
def delete(id):
    # TODO CHECK ROLE
    discipline.delete_discipline_by_id(id)
    flash("Discipline deleted")
    return redirect(url_for("disciplines.list"))


class DisciplineForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    category = StringField('Category', [validators.Length(min=4, max=25)])
    coach = StringField('Instructors Name', [validators.Length(min=4, max=25)])
    schedule = StringField('Schedule', [validators.Length(min=4, max=25)])
    monthly_price = StringField('monthly_price', [validators.Length(min=4, max=25)])
    active = BooleanField('active')