from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import member as Member
from wtforms import Form, SelectField, StringField, PasswordField, validators
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
    print(input)

    if form.select.data == "member_id":
        # If user is searched by member_id, either there is a member with that id or there is none
        member = Member.search_by_id(input)
        #TODO fix this: if input is not a number, it will return sql error 
        if member:
            print(f"member found: {member.first_name}")
            return redirect(url_for("payments.invoices", id=input))

    elif form.select.data == "last_name":
        # There could be multiple Gonzalez, it is unfair only one is paying
        members = Member.search_by_last_name(input)
        for member in members:
            print(f"member found: {member.first_name}")
        if members:
            #TODO fix this: payments.results does not recognize both parameters
            return redirect(
                url_for("payments.results", last_name=input, members=members)
            )

    flash(f"No se han encontrado miembros con apellido {input}", "danger")
    return redirect(url_for("payments.index"))


@payments_blueprint.get("/search/results/")
def results(last_name, members):
    print(f"last_name: {last_name}")
    return render_template(
        "payments/results.html", members=members, last_name=last_name
    )


@payments_blueprint.get("/<int:id>/invoices")
def invoices(id):
    member=Member.search_by_id(id)

    #TODO this obviously has issues, check later how to do it
    last_invoice = Payments.lastInvoice(id)
    if last_invoice == date.today().month or (not last_invoice and date.today().day < 11):
        createInvoice(id)

    invoices = Payments.member_invoices(id)
    return render_template("payments/invoices.html", member=member, invoices=invoices)

def createInvoice(member_id):
    base_price= 100
    total_price = base_price 
    member_number= member_id
    Payments.createInvoice(member_number=member_number, total_price=total_price, base_price=base_price)


@payments_blueprint.get("/<int:id>/invoice/<invoice_id>")
def show_invoice(invoice_id):
    # TODO: show invoice information and payment button
    pass


@payments_blueprint.post("/<int:id>/invoice/<invoice_id>/pay")
def pay_invoice(invoice_id):
    # TODO: pay invoice, generate payment and redirect to invoice page with a success message
    pass


@payments_blueprint.get("/<int:id>/payment/<payment_id>/")
def download(payment_id):
    # TODO: download payment PDF
    pass


class UserSearchForm(Form):
    choices = [
        ("member_id", "ID del miembro"),
        ("last_name", "Apellido"),
    ]
    select = SelectField("Buscar por:", choices=choices)
    search = StringField(
        "", [validators.Length(min=1, max=15), validators.DataRequired()]
    )
