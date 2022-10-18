import click
from flask import Blueprint
from src.core.auth import users, role, user_role, permission,role_permission
from src.core.discipline import discipline, member_discipline
from src.core.system_config import system_config
from src.core import database, seeds

from src.core.auth import *

usersbp = Blueprint('user', __name__)
seedsbp = Blueprint('seeds', __name__)
databasebp = Blueprint('database', __name__)

# Users ------------
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

@databasebp.cli.command(name="create_tables")
def create_tables():
    """ Creates missing tables """
    database.create_tables()

@databasebp.cli.command(name="reset")
def resetdb():
    """ Resets the database """
    database.reset_db()

@databasebp.cli.command(name="drop")
def dropdb():
    """ Drops all tables """
    database.drop_db()

# Seeds commands -------
@seedsbp.cli.command(name="initialize")
def seedsdb():
    seeds.run()