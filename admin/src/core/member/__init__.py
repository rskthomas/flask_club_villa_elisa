"""Module dedicated to Member handling such as CRUDs

"""
from os import abort
from sqlite3 import InternalError
from sqlalchemy.exc import IntegrityError
from src.core.member.member import Member
from src.core.database import db
from src.core.utils import paginated


class IntegrytyException(Exception):
    pass


def list_members(filter={}):
    """Get current list of members based on the receive filter

    Args:
        filter (dict, optional): querying criteria. Possible keys:
        -last_name
        -membership)state
        -personal_id
        Defaults to {}.

    Returns:
        list: list of Member
    """
    query = Member.query
    if filter.get('last_name'):
        query = query.where(
            Member.last_name.ilike(
                "%" + filter['last_name'] + '%'))
    if filter.get('membership_state') is not None:
        query = query.where(Member.membership_state ==
                            filter['membership_state'])
    if filter.get('personal_id'):
        query = query.where(Member.personal_id.ilike(
            f"%{ filter.get('personal_id') }%"))
    return query


def create_member(**kwargs):
    """Create a new Member

    Args:
        kwargs: all fields of object Member

    Raises:
        IntegrytyException: raised if ocurrs IntegrityError for ex: "unique fields violation"
    """
    try:
        member = Member(**kwargs)
        db.session.add(member)
        db.session.commit()
        return member
    except IntegrityError:
        db.session.rollback()
        raise IntegrytyException


def update_member(id, **kwargs):
    """Update a Member

    Args:
        id(int): identifier of Member
        args: fields to update

    Raises:
        IntegrytyException: raised if ocurrs IntegrityError for ex: "unique fields violation"
    """
    try:
        member = find_member(id)
        for key, value in kwargs.items():
            setattr(member, key, value)
        db.session.commit()
        return member
    except IntegrityError:
        db.session.rollback()
        raise IntegrytyException


def delete_member(id):
    """Deletes a member by its id

    Args:
        id (int): id of the member to be deleted

    Returns:
        Member: member recently deleted
    """
    member = find_member(id)
    db.session.delete(member)
    db.session.commit()
    return member


def find_member(id):
    """Looks up for a member on the DB based on the received id

    Args:
        id (int): id of the member

    Returns:
        Member: member from the DB
    """
    return Member.query.get(id)


def delete_member_by_member_number(mem_number):
    """deletes a member by its number

    Args:
        mem_number (int): number of the member
    """
    Member.query.filter(Member.member_number == mem_number).delete()
    db.session.commit()


def find_member_by_lastname(lastname):
    """looks up for a member on the db based on received last name

    Args:
        lastname (str): last name of the member

    Returns:
        list: list of Member matching received lastname
    """
    return Member.query.filter_by(last_name=lastname)


def find_member_by_state(state):
    """looks up a member by its current state

    Args:
        state (string): state of the member membership

    Returns:
        list: Members matching
    """
    return Member.query.filter_by(membership_state=state)


def paginated_members(filter={}, current_page=1):
    """
        Paginates Member from the db based on filter and returns current page
        received. Page size relies on system config

    Args:
        filter (dict, optional): filters to be used, same as list_members().
        Defaults to {}.
        current_page (int, optional): pagination page to be returned.
            Defaults to 1.

    Returns:
        dict: paginated results. Have 3 keys
            items: Members of the current page
            pages: # of pages based on the page size
    """
    return paginated(list_members(filter), current_page)


def get_member_disciplines(member_id):
    """Get a list of the disciplines of the meber

    Args:
        member_id (int): id of the member

    Returns:
        list: Disciplines associated to the member
    """
    member = find_member(member_id)
    return member.disciplines
