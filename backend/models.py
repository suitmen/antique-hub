from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

# Определение перечислений
class UserRole(str, enum.Enum):
    buyer = "buyer"
    seller = "seller"
    admin = "admin"

class LotStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class OrderStatus(str, enum.Enum):
    created = "created"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"

class TicketStatus(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class TicketCategory(str, enum.Enum):
    payment = "payment"
    item = "item"
    account = "account"
    delivery = "delivery"

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_seller = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.buyer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    lots = relationship("Lot", back_populates="owner")
    orders = relationship("Order", back_populates="buyer")
    tickets = relationship("SupportTicket", back_populates="user")

# Модель лота
class Lot(Base):
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    price = Column(Numeric(12, 2))
    currency = Column(String(3), default="RUB")
    category = Column(String(50))
    era = Column(String(100))
    material = Column(String(100))
    image_urls = Column(JSON)
    is_approved = Column(Boolean, default=False)
    status = Column(Enum(LotStatus), default=LotStatus.pending)
    seller_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    owner = relationship("User", back_populates="lots")
    orders = relationship("Order", back_populates="lot")
    tickets = relationship("SupportTicket", back_populates="lot")

# Модель заказа
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("lots.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.created)
    payment_id = Column(String(100))
    payment_provider = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    lot = relationship("Lot", back_populates="orders")
    buyer = relationship("User", back_populates="orders")

# Модель тикета поддержки
class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String(255))
    message = Column(Text)
    category = Column(Enum(TicketCategory))
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.new)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    user = relationship("User", back_populates="tickets")
    lot = relationship("Lot", back_populates="tickets")