from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4 
from enum import Enum

class Gender (str,Enum): 
    male = "male"
    female = "female"

class Role (str,Enum): 
    admin = "admin"
    user = "user"
    student = "student"

class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name:Optional[str] = None
    gender: Gender
    role: List[Role]
    

# Update model
class UserUpdate(BaseModel):
    first_name: Optional[str] 
    last_name: Optional[str] 
    middle_name: Optional[str] 
    role: Optional[List[Role]] 