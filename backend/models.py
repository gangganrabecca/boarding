from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

# User models
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    role: Literal["user", "admin"] = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: str
    role: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

# Room models
class RoomBase(BaseModel):
    room_number: str
    room_type: str
    capacity: int
    price: float

class RoomCreate(RoomBase):
    status: Literal["available", "occupied", "maintenance"] = "available"

class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    capacity: Optional[int] = None
    price: Optional[float] = None
    status: Optional[Literal["available", "occupied", "maintenance"]] = None

class Room(RoomBase):
    id: str
    status: str
    created_at: datetime

# Booking models
class BookingBase(BaseModel):
    room_id: str
    start_date: str
    end_date: str
    duration: int

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration: Optional[int] = None
    status: Optional[Literal["pending", "approved", "rejected", "cancelled"]] = None

class Booking(BookingBase):
    id: str
    status: str
    created_at: datetime

# Tenant models
class TenantBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    room_id: str

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    id: str
    created_at: datetime

# Notification models
class NotificationBase(BaseModel):
    message: str
    type: str

class NotificationUpdate(BaseModel):
    status: Optional[Literal["pending", "approved", "rejected", "read"]] = None

class Notification(NotificationBase):
    id: str
    status: str
    created_at: datetime
