from fastapi import FastAPI, Depends, HTTPException
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
    allow_origins=["*"],  # В production нужно указать конкретные origins
    allow_credentials=True,
    allow_methods=["*"],
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

# Лоты
@app.post("/lots/", response_model=schemas.Lot)
def create_lot(lot: schemas.LotCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    return crud.create_lot(db=db, lot=lot, user_id=current_user.id)

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
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}