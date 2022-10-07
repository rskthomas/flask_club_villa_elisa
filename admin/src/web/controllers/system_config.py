from flask import Blueprint, render_template, request
from src.core.system_config import getSystemConfig, updateSystemConfig
system_config_blueprint = Blueprint('system_config', __name__, url_prefix ='/configuracion')

@system_config_blueprint.get("/")
def show():
  return render_template('system_config/show.html', system_config=getSystemConfig())

@system_config_blueprint.get("/editar")
def edit():
  return render_template('system_config/edit.html', system_config=getSystemConfig())

@system_config_blueprint.post("/update")
def update():
  params = request.form
  update_args = {}
  update_args["items_qty_for_grids"] = params.get("items_qty_for_grids")
  update_args["public_payments_available"] = params.get("public_payments_available") == "on"
  update_args["public_contact_info_available"] = params.get("public_contact_info_available")  == "on"
  update_args["payment_header_text"] = params.get("payment_header_text")
  update_args["base_monthly_fee"] = params.get("base_monthly_fee")
  update_args["delayed_payment_interests_rate"] = float(params.get("delayed_payment_interests_rate")) / 100

  updateSystemConfig(update_args)
  return show()