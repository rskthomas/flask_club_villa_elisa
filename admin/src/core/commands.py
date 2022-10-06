import click
from flask import Blueprint
from src.core.auth.users import User
from src.core import database

from src.core.auth import *

usersbp = Blueprint('users', __name__)

databasebp = Blueprint('database', __name__)

@usersbp.cli.command('create')
@click.argument('name')
@click.argument('email')
@click.argument('password')
def create(name, email, password):
    """ Creates a user """
    print("Create user: {}".format(name))
    create_user(firstname=name, email=email, password=password)

@usersbp.cli.command('delete')
@click.argument('name')
def delete(name):
    """ deletes a user """
    print("Delete user: {}".format(name))
    delete_user_by_name(firstname=name)


@databasebp.cli.command(name="reset")
def resetdb():
    """ Resets the database """
    database.reset_db()

@databasebp.cli.command(name="drop")
def dropdb():
    """ Drops all tables """
    database.drop_db()