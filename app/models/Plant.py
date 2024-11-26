from sqlalchemy import Column,Integer,String,Text
from app.DBHandler import Base

class Plant(Base):
    __tablename__ = "Plants"
    plant_id = Column(Integer, primary_key=True, index=True)
    nursery_id=Column(Integer,index=True)
    name=Column(String(200),nullable=False,index=True)
    description=Column(Text)
    price=Column(String,index=True)
    stock=Column(Integer,default=0,index=True)
    image_url=Column(Text)