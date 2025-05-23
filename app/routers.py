# routers.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import *
from schemas import *
from dbutils import *
from middleware import *
from database import get_db
from typing import List

router = APIRouter(
    prefix="/order",
    tags=["order"]
)

###################################
##### Routers Functions Below #####
###################################

#Function for order creation based on a json DTO
#Input: OrderCreateDTO, auth token
#Output: OrderReadDTO
@router.post("", response_model=OrderReadDTO, status_code=201)
async def order_register(payload: OrderCreateDTO, db: Session = Depends(get_db),
                           cookie: AuthToken = Depends(get_cookie_as_model)):
    try:        
        order = create_order(db, payload, cookie.id)
        return order
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Function for getting all orders
#Input: auth token
#Output: List[OrderReadDTO]
@router.get("", response_model=List[OrderShortReadDTO], status_code=200)
async def show_all_orders_by_user(db: Session = Depends(get_db),
                            cookie: AuthToken = Depends(get_cookie_as_model)):
    try:        
        orders = get_all_orders_by_user(db, cookie.id)
        return orders
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Function for getting a order
#Input: id, auth token
#Output: OrderReadDTO
@router.get("/{id}", response_model=OrderReadDTO, status_code=200)
async def get_single_orders(id: int, db: Session = Depends(get_db),
                              cookie: AuthToken = Depends(get_cookie_as_model)):
    try:        
        order = get_order_by_id(db, id, cookie.id)
        return order
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    