#models.py
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Time, ForeignKey, CheckConstraint, UniqueConstraint, 
    SmallInteger, Table, DateTime, Float
)

Base = declarative_base()

# Association Table for Order <-> Product (many-to-many)
class Password(Base):
    __tablename__ = 'password'

    id = Column(Integer, primary_key=True, autoincrement=True)
    password256 = Column(String(256), nullable=False)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)
    id_password = Column(Integer, ForeignKey('password.id'))

    password = relationship("Password")

    __table_args__ = (
        UniqueConstraint('id_password'),
    )

    orders = relationship("Order", back_populates="user")

order_product_table = Table(
    'order_product',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('order.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
    Column('quantity', Float, nullable=False),
    Column('total_price', Float, nullable=False)
)


class Product(Base):
    __tablename__ = 'product'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), nullable=False, unique=True)
    price = Column(Float(8), nullable=False)
    unit = Column(String(12), nullable=False)



class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    date = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="orders")
    products = relationship(
        "Product",
        secondary=order_product_table,
        backref="orders"
    )