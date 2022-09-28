from src.core.auth import create_user

import click
from flask import Blueprint

from src.core.auth.users import User
from src.core import database

usersbp = Blueprint('users', __name__)

databasebp = Blueprint('database', __name__)

@usersbp.cli.command('create')
@click.argument('name')
def create(name):
    """ Creates a user """
    print("Create user: {}".format(name))
    create_user(firstname=name)


@databasebp.cli.command(name="reset")
def resetdb():
    database.reset_db()