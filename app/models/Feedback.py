from app.DBHandler import Base
from sqlalchemy import Column, Integer, Text, Date

class Feedback(Base):
    __tablename__ = 'Feedback'

    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer)
    comment = Column(Text)
    created_at = Column(Date)