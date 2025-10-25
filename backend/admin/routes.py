from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import schemas
import admin.schemas as admin_schemas
import admin.crud as crud
import models, database, auth
from io import StringIO
import csv

router = APIRouter(prefix="/admin", tags=["admin"])

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Проверка прав администратора
def check_admin(current_user: models.User = Depends(auth.get_current_active_user)):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

# Пользователи
@router.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_update: admin_schemas.AdminUserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Лоты
@router.get("/lots/", response_model=List[schemas.Lot])
def read_lots(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    lots = crud.get_lots(db, skip=skip, limit=limit)
    return lots

@router.put("/lots/{lot_id}", response_model=schemas.Lot)
def update_lot(
    lot_id: int,
    lot_update: admin_schemas.AdminLotUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    db_lot = crud.update_lot(db, lot_id=lot_id, lot_update=lot_update)
    if db_lot is None:
        raise HTTPException(status_code=404, detail="Lot not found")
    return db_lot

@router.delete("/lots/{lot_id}")
def delete_lot(
    lot_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    db_lot = crud.delete_lot(db, lot_id=lot_id)
    if db_lot is None:
        raise HTTPException(status_code=404, detail="Lot not found")
    return {"message": "Lot deleted successfully"}

# Заказы
@router.get("/orders/", response_model=List[schemas.Order])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

# Тикеты поддержки
@router.get("/tickets/", response_model=List[schemas.SupportTicket])
def read_tickets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    tickets = crud.get_tickets(db, skip=skip, limit=limit)
    return tickets

@router.put("/tickets/{ticket_id}", response_model=schemas.SupportTicket)
def update_ticket(
    ticket_id: int,
    ticket_update: admin_schemas.AdminTicketUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    db_ticket = crud.update_ticket(db, ticket_id=ticket_id, ticket_update=ticket_update)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

# Экспорт данных
@router.get("/export/users")
def export_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    users = crud.export_users(db)
    
    # Создание CSV данных
    output = StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow(["ID", "Email", "Is Seller", "Verified", "Role", "Created At"])
    
    # Данные
    for user in users:
        writer.writerow([
            user.id,
            user.email,
            user.is_seller,
            user.verified,
            user.role,
            user.created_at
        ])
    
    return {"data": output.getvalue()}

@router.get("/export/lots")
def export_lots(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    lots = crud.export_lots(db)
    
    # Создание CSV данных
    output = StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow(["ID", "Title", "Price", "Currency", "Category", "Seller ID", "Approved", "Status", "Created At"])
    
    # Данные
    for lot in lots:
        writer.writerow([
            lot.id,
            lot.title,
            lot.price,
            lot.currency,
            lot.category,
            lot.seller_id,
            lot.is_approved,
            lot.status,
            lot.created_at
        ])
    
    return {"data": output.getvalue()}

@router.get("/export/orders")
def export_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    orders = crud.export_orders(db)
    
    # Создание CSV данных
    output = StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow(["ID", "Item ID", "Buyer ID", "Status", "Payment ID", "Payment Provider", "Created At"])
    
    # Данные
    for order in orders:
        writer.writerow([
            order.id,
            order.item_id,
            order.buyer_id,
            order.status,
            order.payment_id,
            order.payment_provider,
            order.created_at
        ])
    
    return {"data": output.getvalue()}

@router.get("/export/tickets")
def export_tickets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(check_admin)
):
    tickets = crud.export_tickets(db)
    
    # Создание CSV данных
    output = StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow(["ID", "User ID", "Subject", "Category", "Order ID", "Status", "Created At"])
    
    # Данные
    for ticket in tickets:
        writer.writerow([
            ticket.id,
            ticket.user_id,
            ticket.subject,
            ticket.category,
            ticket.order_id,
            ticket.status,
            ticket.created_at
        ])
    
    return {"data": output.getvalue()}