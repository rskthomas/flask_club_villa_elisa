from sqlalchemy import update
from src.core.auth.users import User
from src.core.auth.role import Role
from src.core.database import db


def list_user():
    return User.query.all()


def create_user(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def delete_user_by_name(firstname):
    User.query.filter(User.firstname == firstname).delete()
    db.session.commit()


def update_user(id, args, role_ids=None):
    if role_ids is not None:
        user = User.query.filter_by(id=id).first()
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        user.roles = roles
        db.session.commit()

    db.session.execute(
        update(User)
        .where(User.id == id)
        .values(args)
    )

    db.session.commit()
    return


def find_user(id):
    return User.query.filter_by(id=id).first()


def find_user_by_mail_and_pass(email, password):
    return User.query.filter_by(email=email, password=password).first()

def list_roles():
    return Role.query.all()