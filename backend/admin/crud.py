from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
from admin import schemas as admin_schemas

# Админские CRUD операции для пользователей
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: int, user_update: admin_schemas.AdminUserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Админские CRUD операции для лотов
def get_lots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lot).offset(skip).limit(limit).all()

def get_lot(db: Session, lot_id: int):
    return db.query(models.Lot).filter(models.Lot.id == lot_id).first()

def update_lot(db: Session, lot_id: int, lot_update: admin_schemas.AdminLotUpdate):
    db_lot = get_lot(db, lot_id)
    if db_lot:
        update_data = lot_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_lot, key, value)
        db.commit()
        db.refresh(db_lot)
    return db_lot

def delete_lot(db: Session, lot_id: int):
    db_lot = get_lot(db, lot_id)
    if db_lot:
        db.delete(db_lot)
        db.commit()
    return db_lot

# Админские CRUD операции для заказов
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

# Админские CRUD операции для тикетов поддержки
def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SupportTicket).offset(skip).limit(limit).all()

def get_ticket(db: Session, ticket_id: int):
    return db.query(models.SupportTicket).filter(models.SupportTicket.id == ticket_id).first()

def update_ticket(db: Session, ticket_id: int, ticket_update: admin_schemas.AdminTicketUpdate):
    db_ticket = get_ticket(db, ticket_id)
    if db_ticket:
        update_data = ticket_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ticket, key, value)
        db.commit()
        db.refresh(db_ticket)
    return db_ticket

# Экспорт данных
def export_users(db: Session) -> List[admin_schemas.ExportUser]:
    users = db.query(models.User).all()
    return [admin_schemas.ExportUser.from_orm(user) for user in users]

def export_lots(db: Session) -> List[admin_schemas.ExportLot]:
    lots = db.query(models.Lot).all()
    return [admin_schemas.ExportLot.from_orm(lot) for lot in lots]

def export_orders(db: Session) -> List[admin_schemas.ExportOrder]:
    orders = db.query(models.Order).all()
    return [admin_schemas.ExportOrder.from_orm(order) for order in orders]

def export_tickets(db: Session) -> List[admin_schemas.ExportTicket]:
    tickets = db.query(models.SupportTicket).all()
    return [admin_schemas.ExportTicket.from_orm(ticket) for ticket in tickets]