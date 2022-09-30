from src.core.auth.users import User
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
    