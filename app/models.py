from sqlalchemy import Column, Enum as SQLEnum, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Mapped, relationship
from database import Base
from enum import Enum

class OrderStatus(str,Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    email = Column(String(256), unique=True, index=True, nullable=False)
    telephone = Column(String(20), nullable=True)
    hashed_password = Column(String, nullable=False) 
    orders = relationship("Order", back_populates="user_owner")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"))
    quantity = Column(Integer, nullable=False)
    user_owner = relationship("User", back_populates="orders") 
    product_details = relationship("Product")
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus, name="order_status_enum"),
        nullable=False,
        default=OrderStatus.pending 
    )


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    group = Column(String(128), nullable=True)
    price = Column(Integer, nullable=False)

\


