""" Module that handles overal system configuration

"""
from sqlalchemy import update
from src.core.system_config.system_config import SystemConfig
from src.core.database import db

def get_system_config():
    """Get system config"""
    return SystemConfig.query.first()


def update_system_config(args):
    """Update system config

    Args:
        args (dictionary): arguments to update

    Returns:
        SystemConfig: returns the updated system configuration
    """
    db.session.execute(update(SystemConfig).values(args))
    db.session.commit()
    return


def get_monthly_fee():
    """Returns the base monthly fee

    Returns:
        float: monthly fee set up on DB
    """
    return SystemConfig.query.first().base_monthly_fee


def get_recharge_percentage():
    """Returns the recharge percentage, for a user that is late on payment

    Returns:
        float: _description_
    """
    return SystemConfig.query.first().delayed_payment_interests_rate
