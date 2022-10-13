from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core.payments import invoice as Payment
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from src.web.controllers.auth import login_required


payments_blueprint = Blueprint("payments", __name__, url_prefix="/payments")


@payments_blueprint.get("/")
def user_search():
    # TODO: implement search of users
    pass


@payments_blueprint.post("/search")
def search(request):
    # TODO: search user and redirect to user invoice
    pass


@payments_blueprint.get("/<user_id>/invoices")
def show_invoices(user_id):
    # TODO: show all unpaid invoices, each with a button to go to payment page
    # TODO: show all paid invoices with a button to download payment PDF
    pass


@payments_blueprint.get("/<user_id>/invoice/<invoice_id>")
def show_invoice(invoice_id):
    # TODO: show invoice information and payment button
    pass


@payments_blueprint.post("/<user_id>/invoice/<invoice_id>/pay")
def pay_invoice(invoice_id):
    # TODO: pay invoice, generate payment and redirect to invoice page with a success message
    pass


@payments_blueprint("/<user_id>/payment/<payment_id>/", methods=["GET", "POST"])
def download(payment_id):
    # TODO: download payment PDF
    pass
