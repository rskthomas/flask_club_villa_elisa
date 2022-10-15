from src.web.helpers.handlers import bad_request
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for
from flask import session
from src.core import member as Member
from wtforms import Form, SelectField, StringField, PasswordField, validators
from src.web.controllers.auth import login_required
from src.core import payments as Payments


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
            invoices = Payments.member_invoices(input)
            print(f"member invoices: {invoices}")
            return redirect(url_for("payments.invoices", id=input, invoices=invoices))

    elif form.select.data == "last_name":
        # There could be multiple Gonzalez, it is unfair only one is paying
        members = Member.search_by_last_name(input)
        for member in members:
            print(f"member found: {member.first_name}")
        if members:
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
def invoices(id, invoices=None):
    # TODO: show all unpaid invoices, each with a button to go to payment page
    # TODO: show all paid invoices with a button to download payment PDF
    # if invoices is None: list is empty
    return f"Acá se muestra facturas para el usuario{id}"


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
