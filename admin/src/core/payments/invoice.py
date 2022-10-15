from src.core.database import db

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    year = db.Column(db.Integer(), nullable=False, default=db.func.year())
    month = db.Column(db.Integer(), nullable=False, default=db.func.month())
    base_price = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.String(50), nullable=False)
    paid = db.Column(db.Boolean(), default=False)
    member_number = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    payment = db.relationship("Payment", backref="invoice", lazy=True, nullable=True)
    #TODO implement extra items when discipline enrollment is finished

class invoice_extra_item(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    description = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.String(50), nullable=False)
    payment_date = db.Column(db.DateTime(), default=db.func.now())
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)