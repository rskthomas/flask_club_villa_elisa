"""
Module to handle CRUD of disciplines

"""
from src.core.member.member import Member
from src.core.discipline.discipline import Discipline
from src.core.database import db
from src.core.member import find_member


class InactiveDiscipline(Exception):
    pass


class InactiveMember(Exception):
    pass


class MemberNotFound(Exception):
    pass


class DisciplineNotFound(Exception):
    pass


def get_disciplines():
    """Get the list of all disciplines

    Returns:
        list: list of Discipline records on DB
    """
    return Discipline.query.all()


def create_discipline(**kwargs):
    """ Creates a new discipline on the DB based on received params
        Allowed params can be checked at discipline.py

    Returns:
        Discipline: recently created discipline
    """
    discipline = Discipline(**kwargs)
    db.session.add(discipline)
    db.session.commit()
    return discipline


def delete_discipline(id):
    """Deletes a discipline by received id

    Args:
        id (int): id of the Discipline to be removed

    Returns:
        Discipline: recently removed discipline
    """
    discipline = find_discipline(id)
    db.session.delete(discipline)
    db.session.commit()
    return discipline


def find_discipline(id):
    """looks up Discipline by id on the DB

    Args:
        id (int): id of the discipline to be looked up

    Returns:
        Discipline: Discipline record from DB
    """
    return Discipline.query.get(id)


def update_discipline(id, **kwargs):
    """Updates dicipline attributes

    Args:
        id (int): id of the discipline to be updated

    Returns:
        Discipline: updated discipline
    """
    discipline = find_discipline(id)
    for key, value in kwargs.items():
        setattr(discipline, key, value)
    db.session.commit()
    return discipline


def enroll_member(discipline_id, member_id):
    """Enrolls a user to a discipline if both are active

    Args:
        discipline_id (int): id of the discipline
        member_id (int): id of the discipline

    Raises:
        InactiveDiscipline: raised if the discipline is not active
        InactiveMember: raised if the member is not active
    """
    discipline = find_discipline(discipline_id)
    if not discipline.active:
        raise InactiveDiscipline()
    member = find_member(member_id)
    if not member.membership_state:
        raise InactiveMember
    discipline.members.append(member)
    db.session.commit()


def cancel_enrollment(discipline_id, member_id):
    """Cancel a member enrollment to a discipline

    Args:
        discipline_id (int): id of the discipline
        member_id (int): id of the member

    Raises:
        DisciplineNotFound: raised if the discipline is not found
        MemberNotFound: raised if the member is not found
    """
    discipline = find_discipline(discipline_id)
    if not discipline:
        raise DisciplineNotFound
    member = find_member(member_id)
    if not member:
        raise MemberNotFound
    discipline.members.remove(member)
    db.session.commit()


def get_members(discipline_id):
    """returns a list of Member enrolled to the received discipline

    Args:
        discipline_id (int): Dicipline id

    Returns:
        list: list of Member enrolled to the discipline
    """
    discipline = find_discipline(discipline_id)
    return discipline.members
