from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from src.core.auth.users import User
from src.core.auth.role import Role
from src.core.auth.user_role import UserRole
from src.core.auth.role_permission import RolePermission
from src.core.auth.permission import Permission
from src.core.utils import paginated
from src.core.database import db

class IntegrytyException(Exception):
    pass

def base_user_query(filter={}):
    """
        Builds sqlalchemy query for User modelwithout fetching the results.

    Args:
        filter (dict, optional): query filters. email and active keys accepted
        Defaults to {}.

    Returns:
        flask_sqlalchemy.BaseQuery
    """
    query = User.query
    if filter.get('email'):
        query = query.where(User.email.ilike("%" + filter['email'] + '%'))
    if filter.get('active') is not None:
        query = query.where(User.active == filter['active'])

    return query


def paginated_users(filter={}, current_page=1):
    """
        Paginates users from the db based on filter and returns current page
        received. Page size relies on system config

    Args:
        filter (dict, optional): filters to be used, same as base_user_query.
        Defaults to {}.
        current_page (int, optional): pagination page to be returned.
            Defaults to 1.

    Returns:
        dict: paginated results. Have 3 keys
            items: users of the current page
            pages: # of pages based on the page size
    """
    return paginated(base_user_query(filter), current_page)


def list_user(filter={}):
    return base_user_query(filter).all();


def create_user(**kwargs):
    """Create a new User

    Args:
        kwargs: all fields of object Member 

    Raises:
        IntegrytyException: raised if ocurrs IntegrityError for ex: "unique fields violation"
    """
    try:
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user
    except IntegrityError:
        db.session.rollback()
        raise IntegrytyException    


def delete_user_by_name(firstname):
    User.query.filter(User.firstname == firstname).delete()
    db.session.commit()


def update_user(id, args):
    """Update a User

    Args:
        id: identifier of user
        args: fields to update 

    Raises:
        IntegrytyException: raised if ocurrs IntegrityError for ex: "unique fields violation"
    """
    try:
        db.session.execute(
            update(User)
            .where(User.id == id)
            .values(args)
            .returning(User.id)
        )

        db.session.commit()
        return
    except IntegrityError:
        db.session.rollback()
        raise IntegrytyException  
        

def delete_user(user_id):
    db.session.query(User).filter(User.id==user_id).delete()
    db.session.commit()
    return


def find_user(id):
    return User.query.filter_by(id=id).first()


def find_user_by_mail_and_pass(email, password):
    return User.query.filter_by(email=email, password=password).first()


def list_roles():
    return Role.query.all()

def update_user_roles(user, role_ids):
    roles = Role.query.filter(Role.id.in_(role_ids)).all()
    user.roles = roles
    db.session.commit()
    return

def can_perform(user_id, permission_name):
    return any(
        User.query
        .join(UserRole)
        .join(RolePermission, UserRole.role_id == RolePermission.role_id)
        .join(Permission).where(User.id == user_id)
        .where(Permission.name == permission_name)
    )
