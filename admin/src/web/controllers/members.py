from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import member


member_blueprint = Blueprint("member", __name__, url_prefix="/member")

@member_blueprint.get("/")
def member_index():
  member = []
  return render_template('members/index.html', members=member)
