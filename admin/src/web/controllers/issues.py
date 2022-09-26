from flask import Blueprint, render_template

issue_blueprint = Blueprint('issues', __name__, url_prefix ='/consultas')

@issue_blueprint.get("/")
def issue_index():
  issues = []
  return render_template('issues/index.html', issues=issues)