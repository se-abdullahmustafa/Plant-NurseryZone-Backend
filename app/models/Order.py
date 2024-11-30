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
    
    
class OrderStatusService:
    VALID_STATUSES = [
        "Pending", 
        "Processing", 
        "Shipped", 
        "Delivered", 
        "Cancelled"
    ]

    VALID_TRANSITIONS = {
        "Pending": ["Processing", "Cancelled"],
        "Processing": ["Shipped", "Cancelled"],
        "Shipped": ["Delivered"],
        "Delivered": [],
        "Cancelled": []
    }

    @classmethod
    def validate_status_change(cls, current_status: str, new_status: str) -> bool:
        if new_status not in cls.VALID_STATUSES:
            return False
        return new_status in cls.VALID_TRANSITIONS.get(current_status, [])
    