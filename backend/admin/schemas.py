from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models import UserRole, LotStatus, OrderStatus, TicketStatus

# Админские схемы для пользователей
class AdminUserUpdate(BaseModel):
    is_seller: Optional[bool] = None
    verified: Optional[bool] = None
    role: Optional[UserRole] = None

# Админские схемы для лотов
class AdminLotUpdate(BaseModel):
    is_approved: Optional[bool] = None
    status: Optional[LotStatus] = None

# Админские схемы для тикетов
class AdminTicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None

# Схемы для экспорта данных
class ExportUser(BaseModel):
    id: int
    email: str
    is_seller: bool
    verified: bool
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

class ExportLot(BaseModel):
    id: int
    title: str
    price: float
    currency: str
    category: str
    seller_id: int
    is_approved: bool
    status: LotStatus
    created_at: datetime

    class Config:
        from_attributes = True

class ExportOrder(BaseModel):
    id: int
    item_id: int
    buyer_id: int
    status: OrderStatus
    payment_id: Optional[str] = None
    payment_provider: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ExportTicket(BaseModel):
    id: int
    user_id: int
    subject: str
    category: str
    order_id: Optional[int] = None
    status: TicketStatus
    created_at: datetime

    class Config:
        from_attributes = True