from wtforms import Form, BooleanField, StringField, IntegerField, validators
from wtforms.fields import EmailField


class MemberForm(Form):
    """Represents an html form of Member model"""

    first_name = StringField(
        "Nombre", [
            validators.Regexp('^[A-Za-z]+$', message="Firstname must contain only letters"),  
            validators.Length(min=4, max=50), validators.DataRequired()]
    )
    last_name = StringField(
        "Apellido", [
            validators.Regexp('^[A-Za-z]+$', message="Lastname must contain only letters"),  
            validators.Length(min=4, max=50), validators.DataRequired()])
    personal_id_type = StringField(
        "Tipo Documento",
        [validators.Length(min=1, max=25), validators.DataRequired()],
    )
    personal_id = StringField(
        "Nro. Documento", [
            validators.Regexp('^[0-9]+$', message="Document must contain only numbers"),  
            validators.Length(min=1, max=25), validators.DataRequired()])
    gender = StringField(
        "Género", [validators.Length(min=1, max=25), validators.DataRequired()]
    )
    address = StringField(
        "Dirección", [
            validators.Length(
                min=1, max=255), validators.DataRequired()])
    phone_number = StringField(
        "Teléfono", [
            validators.Regexp('^[0-9]+$', message="Phone number must contain only numbers"),  
            validators.Length(min=1, max=25), validators.DataRequired()])
    email = EmailField(
        "Email",
        [
            validators.Length(min=1, max=50),
            validators.DataRequired(),
            validators.Email(),
        ],
    )

    membership_state = BooleanField("Activo")
