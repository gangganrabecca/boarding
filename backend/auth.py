from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
import logging
from dotenv import load_dotenv
from database import Neo4jConnection

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Setup logger
logger = logging.getLogger(__name__)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Fixed database connection to avoid circular import
_db_connection = None

def get_db_connection():
    global _db_connection
    if _db_connection is None:
        _db_connection = Neo4jConnection(
            os.getenv("NEO4J_URI"),
            os.getenv("NEO4J_USERNAME"),
            os.getenv("NEO4J_PASSWORD")
        )
        _db_connection.connect()
    return _db_connection

# Simple database dependency function for use in auth functions
def get_database_for_auth():
    """Get database connection for auth functions"""
    return Neo4jConnection(
        os.getenv("NEO4J_URI"),
        os.getenv("NEO4J_USERNAME"),
        os.getenv("NEO4J_PASSWORD")
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception

        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        # Use database connection for auth
        db = get_database_for_auth()
        if db.driver is None:
            db.connect()
        user = db.get_user_by_email(email)

        if user is None:
            raise credentials_exception

        return user

    except HTTPException:
        raise  # Re-raise authentication errors
    except Exception as e:
        logger.error(f"Error in get_current_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
