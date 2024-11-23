from app.DBHandler import Base
from sqlalchemy import Integer,Column,Text,String

class Nurseries(Base):
    __tablename__="Nurseries"
    nursery_id=Column(Integer,primary_key=True, index=True)
    user_id=Column(Integer,nullable=False)
    status=Column(Text,index=True,default="Pending",nullable=False)
    