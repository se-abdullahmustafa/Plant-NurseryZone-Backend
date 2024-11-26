from app.DBHandler import Base
from sqlalchemy import Column,Integer,String,DECIMAL,DateTime

class Order(Base):
    __tablename__="Orders"
    order_id=Column(Integer,index=True,primary_key=True)
    user_id=Column(Integer,index=True)
    plant_id=Column(Integer,index=True)
    quantity=Column(Integer)
    total_amount=Column(DECIMAL(10,2))
    status=Column(String(10),default="Pending")
    created_at=Column(DateTime)
    