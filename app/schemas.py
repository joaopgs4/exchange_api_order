# schemas.py
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr

#########################################################################
##### Uses pydantic for cache/dynamic objects; not referenced in DB #####
#########################################################################

#Base JWT AuthToken model
class AuthToken(BaseModel):
    id : int
    username : str
    email : str
    role : Optional[str] = None
    exp : Optional[int] = None  # Optional expiry (timestamp) for the JWT

    # Allow any additional fields
    class Config:
        extra = "allow"

class ProductInOrder(BaseModel):
    id : int
    quantity : int

class OrderCreateDTO(BaseModel):
    items : List[ProductInOrder]

class OrderShortReadDTO(BaseModel):
    id : int
    date : datetime #String of the date-time, as: 2025-10-09T03:21:57
    total : float

class ProductId(BaseModel):
    id : int

class ProductFull(BaseModel):
    id : int
    product : ProductId
    quantity : int
    total : float


class OrderReadDTO(BaseModel):
    id : int
    date : datetime
    items : List[ProductFull]
    total : float