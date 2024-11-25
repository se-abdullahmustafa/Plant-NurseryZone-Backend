from typing import Optional
from pydantic import BaseModel, constr,StringConstraints
from app.schemas.user import  UserResponse

class NurseryBase(BaseModel):
    user_id: int
    status: Optional[str] = 'Pending'
    
class NurseryCreate(NurseryBase):
    pass
class NurseryResponse(NurseryBase):
    nursery_id:int
    class config:
        from_attributes=True
       