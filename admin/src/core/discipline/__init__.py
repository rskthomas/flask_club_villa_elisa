from src.core.discipline.discipline import Discipline 
from src.core.database import db

def get_disciplines():
    return Discipline.query.all()

def create_discipline(**kwargs):
    discipline = Discipline(**kwargs)
    db.session.add(discipline)
    db.session.commit()
    return discipline

def delete_discipline(id):
    Discipline.query.filter(Discipline.id == id).delete()
    db.session.commit()


def find_discipline(id):
    return Discipline.query.filter(Discipline.id == id).first()

def update_discipline(id, **kwargs):
    Discipline.query.filter(Discipline.id == id).first().update(kwargs)
    db.session.commit()
    