from src.core.system_config.system_config import SystemConfig
from src.core.database import db
from sqlalchemy import update


def updateSystemConfig(args):
  return SystemConfig.first()

def getSystemConfig():
  return SystemConfig.query.first()

def updateSystemConfig(args):
  db.session.execute(
    update(SystemConfig)
    .values(args)
  )
  db.session.commit()
  return