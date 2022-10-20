from sqlalchemy import update
from src.core.system_config.system_config import SystemConfig
from src.core.database import db


def update_system_config(args):
  return SystemConfig.first()

def get_system_config():
  return SystemConfig.query.first()

def update_system_config(args):
  db.session.execute(
    update(SystemConfig)
    .values(args)
  )
  db.session.commit()
  return
  
def get_monthly_fee():
  return SystemConfig.query.first().base_monthly_fee

def get_recharge_percentage():
  return SystemConfig.query.first().delayed_payment_interests_rate