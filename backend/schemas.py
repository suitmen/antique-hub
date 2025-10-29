from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from typing import List, Optional
from datetime import datetime
from models import UserRole, LotStatus, OrderStatus, TicketStatus, TicketCategory

# Базовые схемы пользователей
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_seller: bool
    verified: bool
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Схемы токенов
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Входная модель JSON
class LoginRequest(BaseModel):
    email: str
    password: str    

# Базовые схемы лотов
class LotBase(BaseModel):
    title: str
    description: str
    price: float
    currency: str = "RUB"
    category: str
    era: str
    material: str
    image_urls: Optional[List[str]] = None

class LotCreate(LotBase):
    pass

class Lot(LotBase):
    id: int
    is_approved: bool
    status: LotStatus
    seller_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Базовые схемы заказов
class OrderBase(BaseModel):
    item_id: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    buyer_id: int
    status: OrderStatus
    payment_id: Optional[str] = None
    payment_provider: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Базовые схемы тикетов поддержки
class SupportTicketBase(BaseModel):
    subject: str
    message: str
    category: TicketCategory
    order_id: Optional[int] = None

class SupportTicketCreate(SupportTicketBase):
    pass

class SupportTicket(SupportTicketBase):
    id: int
    user_id: int
    status: TicketStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)