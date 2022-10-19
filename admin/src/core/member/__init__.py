from src.core.member.member import Member
from src.core.database import db

def list_members(filter={}):
    """Get a list of all Members"""
    query = Member.query
    if filter.get('last_name'):
        query = query.where(Member.last_name.ilike("%" + filter['last_name'] + '%'))
    if filter.get('membership_state') is not None:
        query = query.where(Member.membership_state == filter['membership_state'])
    if filter.get('personal_id'):
        query = query.where(Member.personal_id.ilike(f"%{ filter.get('personal_id') }%"))
    return query.all()


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
    """Delete a Member by id"""
    Member.query.filter(Member.member_number == mem_number).delete()
    db.session.commit()


def find_member_by_lastname(lastname):
    """Find a Member by last_name"""
    return Member.query.filter_by(last_name=lastname)


def find_member_by_state(state):
    """Find a Member by membership_state"""
    return Member.query.filter_by(membership_state=state)