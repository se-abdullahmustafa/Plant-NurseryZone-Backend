from app.DBHandler import Base
from sqlalchemy import Column, Integer, Text, Date


class DeliveryBoy(Base):
    __tablename__ = 'DeliveryBoy'

    delivery_boy_id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    nursery_id = Column(Integer)
    user_id = Column(Integer)
