from app.DBHandler import Base
from sqlalchemy import Column, Integer, Text, Date

class DeliverySchedule(Base):
    __tablename__ = 'DeliverySchedule'

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, nullable=False)
    delivery_boy_id = Column(Integer,  nullable=False)
    scheduled_date = Column(Date, nullable=False)