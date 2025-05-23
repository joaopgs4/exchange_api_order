#dbutils.py
from sqlalchemy.orm import Session
from typing import List
from datetime import timezone
from models import *
from schemas import *
import hashlib
import os

PASS_SALT=os.getenv("PASS_SALT")
if PASS_SALT is None:
    raise ValueError("Environment variable PASS_SALT is not set.")

def create_order(db: Session, orderDTO: OrderCreateDTO, user_id: int) -> OrderReadDTO:

    new_order = Order(
        user_id=user_id,
        date=datetime.now(timezone.utc)
    )
    db.add(new_order)
    db.flush()  # Get order ID before inserting into association table

    total_order_price = 0
    items_response = []

    for item in orderDTO.items:
        product = db.query(Product).filter(Product.id == item.id).first()

        total_price = product.price * item.quantity
        total_order_price += total_price

        db.execute(order_product_table.insert().values(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            total_price=total_price
        ))

        items_response.append(ProductFull(
            id=product.id,
            product=ProductId(id=product.id),
            quantity=item.quantity,
            total=total_price
        ))

    db.commit()

    return OrderReadDTO(
        id=new_order.id,
        date=new_order.date,
        items=items_response,
        total=total_order_price
    )

# ---- Get Single Order ----
def get_order_by_id(db: Session, order_id: int, user_id: int) -> OrderReadDTO:
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()

    items = []
    total = 0

    result = db.execute(
        order_product_table.select().where(order_product_table.c.order_id == order.id)
    ).fetchall()

    for row in result:
        product = db.query(Product).filter(Product.id == row.product_id).first()
        items.append(ProductFull(
            id=product.id,
            product=ProductId(id=product.id),
            quantity=row.quantity,
            total=row.total_price
        ))
        total += row.total_price

    return OrderReadDTO(
        id=order.id,
        date=order.date,
        items=items,
        total=total
    )

# ---- Get All Orders for a User ----
def get_all_orders_by_user(db: Session, user_id: int) -> List[OrderShortReadDTO]:
    orders = db.query(Order).filter(Order.user_id == user_id).all()

    result = []
    for order in orders:
        order_items = db.execute(
            order_product_table.select().where(order_product_table.c.order_id == order.id)
        ).fetchall()

        total = sum([row.total_price for row in order_items])

        result.append(OrderShortReadDTO(
            id=order.id,
            date=order.date,
            total=total
        ))

    return result