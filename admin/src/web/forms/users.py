from wtforms import Form, BooleanField, StringField, validators, PasswordField
from wtforms.fields import EmailField


class UserForm(Form):
    """Represents an html form of User model"""

    firstname = StringField(
        "Nombre", [validators.Length(min=4, max=50), validators.DataRequired()]
    )
    lastname = StringField(
        "Apellido", [
            validators.Length(
                min=4, max=50), validators.DataRequired()])
    username = StringField(
        "Usuario",
        [validators.Length(min=4, max=50), validators.DataRequired()],
    )
    email = EmailField(
        "Email",
        [
            validators.Length(min=1, max=50),
            validators.DataRequired(),
            validators.Email(),
        ],
    )
    password = PasswordField(
        "Password", [
            validators.Length(
                min=1, max=50), validators.DataRequired()])
    active = BooleanField("Activo")


class EditUserForm(Form):
    """Represents an html form of User model"""

    firstname = StringField(
        "Nombre", [validators.Length(min=4, max=50), validators.DataRequired()]
    )
    lastname = StringField(
        "Apellido", [
            validators.Length(
                min=4, max=50), validators.DataRequired()])
    username = StringField(
        "Usuario",
        [validators.Length(min=4, max=50), validators.DataRequired()],
    )
    email = EmailField(
        "Email",
        [
            validators.Length(min=1, max=50),
            validators.DataRequired(),
            validators.Email(),
        ],
    )
    password = PasswordField(
        "Password", [
            validators.Length(
                min=1, max=50),validators.Optional()])

    active = BooleanField("Activo")
