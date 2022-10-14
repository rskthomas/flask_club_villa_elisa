from src.core.member.member import Member
from src.core.database import db

def list_members():
    """Get a list of all Members"""
    return Member.query.all()

def create_member(**kwargs):
    """Create a new Member"""
    member = Member(**kwargs)
    db.session.add(member)
    db.session.commit()
    return member

def update_member(id, **kwargs):
    """Update a Member"""
    member = find_member(id)
    for key, value in kwargs.items():
        setattr(member, key, value)
    db.session.commit()
    return member

def delete_member(id):
    """Delete a Member by id"""
    member = find_member(id)
    db.session.delete(member)
    db.session.commit()
    return member

def find_member(id):
    """Find a Member by id"""
    return Member.query.get(id)    

def delete_member_by_member_number(mem_number):
    Member.query.filter(Member.member_number == mem_number).delete()
    db.session.commit()

def find_member_by_mail(email):
    return Member.query.filter_by(email=email).first()