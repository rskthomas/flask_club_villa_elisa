import click
from flask import Blueprint
from src.core.auth.users import User
from src.core import database, seeds

from src.core.auth import *

usersbp = Blueprint('users', __name__)
seedsbp = Blueprint('seeds', __name__)
databasebp = Blueprint('database', __name__)

# Users ------------
@usersbp.cli.command('create')
@click.argument('name')
def create(name):
    """ Creates a user """
    print("Create user: {}".format(name))
    create_user(firstname=name)

@usersbp.cli.command('delete')
@click.argument('name')
def delete(name):
    """ deletes a user """
    print("Delete user: {}".format(name))
    delete_user_by_name(firstname=name)

# DB commands -------
@databasebp.cli.command(name="reset")
def resetdb():
    """ Resets the database """
    database.reset_db()

@databasebp.cli.command(name="drop")
def dropdb():
    """ Drops all tables """
    database.drop_db()

# Seeds commands -------
@seedsbp.cli.command(name="seeds")
def seedsdb():
    seeds.run()