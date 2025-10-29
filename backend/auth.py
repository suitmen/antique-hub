from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import User
from database import get_db
from crud import get_user_by_email
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройки JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Настройка OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Добавим отладочную информацию для OAuth2PasswordBearer
async def get_token(token: str = Depends(oauth2_scheme)):
    print(f"OAuth2PasswordBearer received token: {token}")
    return token

# Альтернативный способ получения токена из заголовка
from fastapi import Request
async def get_token_from_header(request: Request):
    authorization = request.headers.get("Authorization")
    print(f"Authorization header: {authorization}")
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        print(f"Extracted token: {token}")
        return token
    return None

# Настройка контекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    print(f"Authenticating user: {email}")
    logger.debug('Авторизация {email} {password}')

    user = get_user_by_email(db, email)
    print(f"User found: {user}")

    if not user:
        print("User not found")
        return False
    
    hashed_pwd = pwd_context.hash(password)
    print(f"Generated hash: {hashed_pwd}")
    print(f"Stored hash: {user.hashed_password}")
    
    if not verify_password(password, user.hashed_password):
        print("Password verification failed")
        return False
    print("Authentication successful")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    print(f"Creating access token for data: {data}")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    print(f"Token payload: {to_encode}")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    print(f"Encoded JWT: {encoded_jwt}")

    return encoded_jwt

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    print(f"get_current_user called")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Получаем токен из заголовка
    token = await get_token_from_header(request)
    if not token:
        print("No token found in Authorization header")
        raise credentials_exception
    
    try:
        print(f"Token received: {token}")
        print(f"SECRET_KEY: {SECRET_KEY}")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload: {payload}")
        
        email: str = payload.get("sub")
        print(f"Email from token: {email}")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"Other error: {e}")
        raise credentials_exception
    
    user = get_user_by_email(db, email=email)
    print(f"User found: {user}")

    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    print(f"get_current_active_user called with: {current_user}")
    if not current_user.verified:
        print("User not verified")
        raise HTTPException(status_code=400, detail="Inactive user")
    print("User is verified, returning user")
    return current_user