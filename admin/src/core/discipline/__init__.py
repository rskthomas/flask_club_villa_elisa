from src.core.discipline.discipline import Discipline 
from src.core.database import db

def get_disciplines():
    """Get a list of all disciplines"""
    return Discipline.query.all()

def create_discipline(**kwargs):
    """Create a new discipline"""
    discipline = Discipline(**kwargs)
    db.session.add(discipline)
    db.session.commit()
    return discipline

def delete_discipline(id):
    """Delete a discipline by id"""
    discipline=find_discipline(id)
    db.session.delete(discipline)
    db.session.commit()
    return discipline

def find_discipline(id):
    """Find a discipline by id"""
    return Discipline.query.get(id)

def update_discipline(id, **kwargs):
    """Update a discipline"""
    discipline = find_discipline(id)
    for key, value in kwargs.items():
        setattr(discipline, key, value)
    db.session.commit()
    return discipline