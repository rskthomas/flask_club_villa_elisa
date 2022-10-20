from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import member as Member
from src.web.forms.payments import UserSearchForm
from src.web.controllers.auth import login_required
from src.core import payments as Payments
from datetime import date


payments_blueprint = Blueprint("payments", __name__, url_prefix="/payments")


@payments_blueprint.get("/")
def index():
    return render_template("payments/user_search.html", form=UserSearchForm())


@payments_blueprint.post("/search")
def search():
    form = UserSearchForm(request.form)
    if not form.validate():
        flash("Hubo un error con el formulario", "danger")
        return redirect(url_for("payments.index"))

    input = form.search.data

    if form.select.data == "member_id":
        route = "payments.invoices"
        member = Member.find_member(input)
    elif form.select.data == "last_name":
        route = "payments.results"
        member = Member.find_member_by_lastname(input)

    if not member:
        flash("No se encontró ningún miembro con ese criterio", "danger")
        return redirect(url_for("payments.index"))

    return redirect(url_for(route, id=input))


@payments_blueprint.get("/search/results/<string:id>")
def results(id):
    last_name = id
    members = Member.find_member_by_lastname(last_name)
    return render_template(
        "payments/results.html", members=members, last_name=last_name
    )


@payments_blueprint.get("/member/<int:id>/invoices")
def invoices(id):
    member = Member.find_member(id)

    last_invoice = Payments.last_invoice(id)
    #If the invoice has not been issued this month, create a new one
    if last_invoice == date.today().month or (
        #Also it should be issued first days of the month
        not last_invoice and date.today().day < 21
    ):
        Payments.create_invoice(member=member)

    invoices = Payments.member_invoices(id)
    return render_template("payments/list.html", member=member, invoices=invoices)


@payments_blueprint.get("/invoice/<int:invoice_id>")
def show_invoice(invoice_id):
    invoice = Payments.get_invoice(invoice_id)
    return render_template("payments/show.html", invoice=invoice)


@payments_blueprint.post("/invoice/<int:invoice_id>/pay")
def pay_invoice(invoice_id):
    payment = Payments.pay_invoice(invoice_id)
    flash("El pago se ha realizado con éxito", "success")

    return redirect(url_for("payments.invoices", id=payment.member_id))


@payments_blueprint.get("/<int:id>/payment/<payment_id>/")
def download(payment_id):
    # TODO: download payment PDF of invoice + payment approved
    pass



