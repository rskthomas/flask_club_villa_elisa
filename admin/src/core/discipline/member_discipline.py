from datetime import datetime
from sqlalchemy import ForeignKey
from src.core.database import db

class MemberDiscipline(db.Model):
  """MemberDiscipline Model that links a member to a discipline"""
  
  __table_name__ = 'member_disciplines'
  member_id = db.Column(db.Integer,
                        ForeignKey('member.id', ondelete="CASCADE"),
                        primary_key=True)
  discipline_id = db.Column(db.Integer,
                        ForeignKey('discipline.id', ondelete="CASCADE"),
                        primary_key=True)
  updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
  created_at = db.Column(db.DateTime, default=datetime.now())
