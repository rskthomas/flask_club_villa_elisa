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