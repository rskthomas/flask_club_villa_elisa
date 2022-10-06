from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import discipline


discipline_blueprint = Blueprint("discipline", __name__, url_prefix="/discipline")

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
    if enabled=="": enabled = "false"

    discipline.create_discipline(name=name, category=category, instructors_name=instructors_name, schedule=schedule, cost=cost, enabled=enabled)
    flash("Discipline created")
    return redirect(url_for("discipline.create"))