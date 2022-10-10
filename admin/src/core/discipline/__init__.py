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
    discipline=find_discipline(id)
    db.session.delete(discipline)
    db.session.commit()
    return discipline

def find_discipline(id):
    return Discipline.query.get(id)

def update_discipline(id, **kwargs):
    discipline = find_discipline(id)
    for key, value in kwargs.items():
        setattr(discipline, key, value)
    db.session.commit()
    return discipline