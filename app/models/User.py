from app.DBHandler import Base
from sqlalchemy import Column, Integer,String,Text

class User(Base):
    __tablename__= "Users"
    user_id = Column(Integer, primary_key=True, index=True)
    role = Column(String,index=True,default="Customer")
    password_hash = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    name=Column(String(20),index=True,nullable=False)
    address=Column(Text,index=True,nullable=False)
    contact_number=Column(String(15),index=True,nullable=False)