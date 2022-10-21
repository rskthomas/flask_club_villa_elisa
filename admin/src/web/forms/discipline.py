from wtforms import Form, BooleanField, StringField, validators, IntegerField


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
    monthly_price = IntegerField("Precio Mensual", [validators.DataRequired()])
    active = BooleanField("Habilitado")
