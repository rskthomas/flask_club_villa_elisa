"""
Module to handle CRUD of disciplines

"""
from sqlalchemy import select, func
from src.core.member.member import Member
from src.core.discipline.discipline import Discipline
from src.core.database import db
from src.core.member import find_member
from src.core.utils import paginated
from collections import defaultdict


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


def paginated_disciplines(current_page=1):
    """
        Paginates Disciplines from the db and returns current page
        received. Page size relies on system config

    Args:
        current_page (int, optional): pagination page to be returned.
            Defaults to 1.

    Returns:
        dict: paginated results. Have 3 keys
            items: Members of the current page
            pages: # of pages based on the page size
    """
    return paginated(Discipline.query, current_page)


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

def enrollment_by_discipline():
    """
        Returns information about enrollments by gender.
        Returned list has the form {
            "Discipline name": {
                    "gender", 12,
                    "gender2": 13
                }
            }


    Returns:
        list: list of disciplines info
    """
    db_rows = db.session.execute(select(Discipline.name, Member.gender, func.count())
        .join(Discipline.members)
        .group_by(Discipline.name, Member.gender))
    result = {}

    for row in db_rows:
        discipline_name = row[0]
        gender_name = row[1]
        gender_count = row[2]
        if result.get(discipline_name) == None:
            result[discipline_name] = {}
        result[discipline_name][gender_name] = gender_count

    return result