from wtforms import (
    Form,
    SelectField,
    StringField,
    validators,
    ValidationError,
)

class UserSearchForm(Form):
    choices = [
        ("member_id", "ID del miembro"),
        ("last_name", "Apellido"),
    ]
    select = SelectField("Buscar por:", choices=choices)
    search = StringField(
        "", [validators.Length(min=1, max=15), validators.DataRequired()]
    )

    def validate_search(form, field):
        """Validates that if member_id is selected, the input is a number"""

        if form.select.data == "member_id" and not field.data.isdigit():
            raise ValidationError("El ID debe ser un número")