from wtforms import Form, BooleanField, StringField, validators

class DisciplineForm(Form):
    """Represents an html form of Discipline model"""

    name = StringField(
        "Nombre", [validators.Length(min=4, max=25), validators.DataRequired()]
    )
    category = StringField(
        "Categoría", [validators.Length(min=4, max=25), validators.DataRequired()]
    )
    coach = StringField(
        "Nombre/s del instructor/es",
        [validators.Length(min=4, max=50), validators.DataRequired()],
    )
    schedule = StringField(
        "Horario", [validators.Length(min=4, max=50), validators.DataRequired()]
    )
    monthly_price = StringField(
        "Precio Mensual", [validators.Length(min=1, max=15), validators.DataRequired()]
    )
    active = BooleanField("Habilitado")