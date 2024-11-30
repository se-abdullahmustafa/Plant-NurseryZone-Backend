from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    order_id:int
    comment:str