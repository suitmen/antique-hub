from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import List, Optional
import models, schemas

# Настройка контекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Пользователи
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_seller=False,
        verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Лоты
def get_lot(db: Session, lot_id: int):
    return db.query(models.Lot).filter(models.Lot.id == lot_id).first()

def get_lots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lot).offset(skip).limit(limit).all()

def create_lot(db: Session, lot: schemas.LotCreate, user_id: int):
    db_lot = models.Lot(
        title=lot.title,
        description=lot.description,
        price=lot.price,
        currency=lot.currency,
        category=lot.category,
        era=lot.era,
        material=lot.material,
        image_urls=lot.image_urls,
        seller_id=user_id
    )
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return db_lot

# Заказы
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    db_order = models.Order(
        item_id=order.item_id,
        buyer_id=user_id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Тикеты поддержки
def get_ticket(db: Session, ticket_id: int):
    return db.query(models.SupportTicket).filter(models.SupportTicket.id == ticket_id).first()

def create_ticket(db: Session, ticket: schemas.SupportTicketCreate, user_id: int):
    db_ticket = models.SupportTicket(
        subject=ticket.subject,
        message=ticket.message,
        category=ticket.category,
        order_id=ticket.order_id,
        user_id=user_id
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket