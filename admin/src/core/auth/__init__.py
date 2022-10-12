from sqlalchemy import update
from src.core.auth.users import User
from src.core.auth.role import Role
from src.core.auth.user_role import UserRole
from src.core.auth.role_permission import RolePermission
from src.core.auth.permission import Permission

from src.core.database import db


def list_user(filter={}):
    query = User.query
    if filter.get('email'):
        query = query.where(User.email.ilike("%" + filter['email'] + '%'))
    if filter.get('active') is not None:
        query = query.where(User.active == filter['active'])

    return query.all()


def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def delete_user_by_name(firstname):
    User.query.filter(User.firstname == firstname).delete()
    db.session.commit()


def update_user(id, args):
    db.session.execute(
        update(User)
        .where(User.id == id)
        .values(args)
        .returning(User.id)
    )

    db.session.commit()
    return


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
