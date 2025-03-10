from datetime import date
import pdfkit
from flask import Blueprint
from flask import render_template
from flask import request, flash, redirect, url_for, make_response
from flask import session
from src.web.helpers.handlers import bad_request
from src.core import member as Member
from src.web.forms.payments import UserSearchForm
from src.web.controllers.auth import login_required
from src.core import payments as Payments
from src.web.helpers.get_header_info import get_header_info


payments_blueprint = Blueprint("payments", __name__, url_prefix="/payments")


@payments_blueprint.get("/")
@login_required('payment_index')
def index():
    """Renders the payment search page for the authenticated user."""
    return render_template(
        "payments/user_search.html",
        form=UserSearchForm(),
        header_info=get_header_info(),
    )


@payments_blueprint.post("/search")
@login_required('payment_index')
def search():
    """Perform the search of member/s specified and return all data to payments index."""
    form = UserSearchForm(request.form)
    if not form.validate():
        flash("Hubo un error con el formulario", "error")
        return redirect(url_for("payments.index"))

    input = form.search.data

    if form.select.data == "member_id":
        route = "payments.invoices"
        member = Member.find_member(input)
    elif form.select.data == "last_name":
        route = "payments.results"
        member = Member.find_member_by_lastname(input)

    if not member:
        flash("No se encontró ningún miembro con ese criterio", "error")
        return redirect(url_for("payments.index"))

    return redirect(url_for(route, id=input))


@payments_blueprint.get("/search/results/<string:id>")
@login_required('payment_index')
def results(id):
    """Return data of all members that fulfill with the lastname specified."""
    last_name = id
    members = Member.find_member_by_lastname(last_name)
    return render_template(
        "payments/results.html",
        members=members,
        last_name=last_name,
        header_info=get_header_info(),
    )


@payments_blueprint.get("/member/<int:id>/invoices")
@login_required('payment_show')
def invoices(id):
    """Renders the invoices of the member id specified and redirect to the payments list view.
    Args:
        id (int): id of the member
    """
    member = Member.find_member(id)

    last_invoice = Payments.last_invoice(id)
    # If the invoice has not been issued this month, create a new one
    if last_invoice == date.today().month or (
        # Also it should be issued first days of the month
        not last_invoice
        and date.today().day < 28
    ):
        Payments.create_invoice(member=member)

    invoices = Payments.member_invoices(id)
    return render_template(
        "payments/list.html",
        member=member,
        invoices=invoices,
        header_info=get_header_info())


@payments_blueprint.get("/invoice/<int:invoice_id>")
@login_required('payment_show')
def show_invoice(invoice_id):
    """Renders the invoice specified and redirect to the payment view.
    Args:
        invoice_id (int): id of invoice
    """
    invoice = Payments.get_invoice(invoice_id)

    # Set photo of receipt of payment
    if invoice.receipt_photo_name:
        receipt = invoice.receipt_photo_name
    else:
        receipt = 'default-receipt-photo.jpg'

    return render_template(
        "payments/show.html", 
        invoice=invoice, 
        header_info=get_header_info(),
        receipt_photo = receipt.strip()
    )


@payments_blueprint.post("/invoice/<int:invoice_id>/pay")
@login_required('payment_update')
def pay_invoice(invoice_id):
    """Make the payment of the invoice specified by parameter
    Args:
        invoice_id (int): id of invoice
    """
    payment = Payments.pay_invoice(invoice_id)
    flash("El pago se ha realizado con éxito", "success")

    return redirect(url_for("payments.invoices", id=payment.member_id))


@payments_blueprint.route("/download/<int:invoice_id>")
@login_required('payment_show')
def download(invoice_id):
    """Render a PDF view of the invoice specified by parameter.
    Args:
        invoice_id (int): id of invoice
    """
    invoice = Payments.get_invoice(invoice_id)

    # Get the HTML output
    out = render_template(
        "payments/export.html", invoice=invoice, header_info=get_header_info()
    )

    # PDF options
    options = {
        "orientation": "landscape",
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
    }

    # Build PDF from HTML
    pdf = pdfkit.from_string(out, options=options)

    # Download the PDF
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "filename=output.pdf"
    return response
