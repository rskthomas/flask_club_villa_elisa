from src.core.member.member import Member
from src.core.database import db

def list_members():
    return Member.query.all()

def create_member(**kwargs):
    mem = Member(**kwargs)
    db.session.add(mem)
    db.session.commit()
    return mem

def delete_member_by_member_number(mem_number):
    Member.query.filter(Member.member_number == mem_number).delete()
    db.session.commit()

def find_member_by_mail(email):
    return Member.query.filter_by(email=email).first()