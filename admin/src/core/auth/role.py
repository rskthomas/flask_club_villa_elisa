from src.core.database import db
from datetime import datetime

class Role(db.Model):
  __table_name = 'roles'
  id = db.Column(db.Integer, primary_key=True, unique=True)
  name = db.Column(db.String(50), nullable=True)
  updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
  created_at = db.Column(db.DateTime, default=datetime.now())
