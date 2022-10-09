from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import discipline


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
    instructors_name = request.form.get("instructors_name")
    schedule = request.form.get("schedule")
    cost = request.form.get("cost")
    enabled = request.form.get("enabled")
    if enabled=="": enabled = False
    else: enabled = True

    discipline.create_discipline(name=name, category=category, instructors_name=instructors_name, schedule=schedule, cost=cost, enabled=enabled)
    flash("Discipline created")
    return redirect(url_for("disciplines.create"))

@discipline_blueprint.get("/update/<int:id>")
def update(id):
  item = discipline.find_discipline_by_id(id)
  return render_template("discipline/update.html", discipline=item)

  
@discipline_blueprint.post("/update/<int:id>")
def update_post(id):
  if not request.form:
    bad_request("No se ha enviado ningun formulario")
  name = request.form.get("name")
  category = request.form.get("category")
  instructors_name = request.form.get("instructors_name")
  schedule = request.form.get("schedule")
  cost = request.form.get("cost")
  enabled = request.form.get("enabled")
  if enabled=="": enabled = False
  else: enabled = True

  discipline.update_discipline(id, name=name, category=category, instructors_name=instructors_name, schedule=schedule, cost=cost, enabled=enabled)
  flash("Discipline updated")
  return redirect(url_for("disciplines.update", id=id))


@discipline_blueprint.post("/delete/<int:id>")
def delete(id):
  #TODO CHECK ROLE
    discipline.delete_discipline_by_id(id)
    flash("Discipline deleted")
    return redirect(url_for("disciplines.list"))