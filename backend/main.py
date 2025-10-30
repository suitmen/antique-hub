from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud, database, auth
import admin.routes as admin_routes

# Создание таблиц в базе данных
database.create_tables()

app = FastAPI(title="AntiqueHub API", description="API для платформы AntiqueHub", version="0.1.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Разрешаем фронтенд
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Подключение маршрутов админки
app.include_router(admin_routes.router)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to AntiqueHub API"}

# Пользователи
@app.get("/users/me", response_model=schemas.User)
async def read_current_user(request: Request, current_user: models.User = Depends(auth.get_current_active_user)):
    print(f"read_current_user called with: {current_user}")
    # Convert the SQLAlchemy model to Pydantic schema
    return schemas.User.model_validate(current_user)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



# Добавим простой endpoint для тестирования токена
@app.get("/test-token")
def test_token(request: Request, current_user: models.User = Depends(auth.get_current_active_user)):
    return {"message": "Token is valid", "user": current_user.email}

# Лоты
@app.post("/lots/", response_model=schemas.Lot)
def create_lot(lot: schemas.LotCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_lot = crud.create_lot(db=db, lot=lot, user_id=current_user.id)
    return schemas.Lot.model_validate(db_lot)

@app.get("/lots/", response_model=List[schemas.Lot])
def read_lots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lots = crud.get_lots(db, skip=skip, limit=limit)
    return lots

@app.get("/lots/{lot_id}", response_model=schemas.Lot)
def read_lot(lot_id: int, db: Session = Depends(get_db)):
    db_lot = crud.get_lot(db, lot_id=lot_id)
    if db_lot is None:
        raise HTTPException(status_code=404, detail="Lot not found")
    return db_lot

# Аутентификация
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.email, form_data.password)

    print(user)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    print(access_token)

    return {"access_token": access_token, "token_type": "bearer"}

# Заказы
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_order = crud.create_order(db=db, order=order, buyer_id=current_user.id)
    return schemas.Order.model_validate(db_order)

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, user_id: int = None, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit, user_id=user_id)
    return orders

# Платежи
@app.post("/payments/init")
def init_payment(item_id: int, currency: str = "RUB", db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    # Здесь должна быть логика инициализации платежа
    # Пока возвращаем заглушку
    return {"redirect_url": f"/payment/{item_id}", "payment_id": f"pay_{item_id}_{current_user.id}"}

# Поддержка
@app.get("/support/tickets", response_model=List[schemas.SupportTicket])
def read_support_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    tickets = crud.get_support_tickets(db, skip=skip, limit=limit, user_id=current_user.id)
    return tickets

@app.post("/support/tickets", response_model=schemas.SupportTicket)
def create_support_ticket(ticket: schemas.SupportTicketCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_ticket = crud.create_support_ticket(db=db, ticket=ticket, user_id=current_user.id)
    return schemas.SupportTicket.model_validate(db_ticket)