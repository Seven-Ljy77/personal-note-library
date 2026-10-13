from pydantic import BaseModel
from datetime import datetime

class RegisterRequest(BaseModel) :
    username : str
    password : str

class RegisterResponse(BaseModel) :
    id : int
    username : str
    created_at : datetime
    is_active : bool

class LoginRequest(BaseModel) :
    username : str
    password : str

class LoginResponse(BaseModel) :
    access_token : str
    refresh_token : str
    token_type : str

class RefreshRequest(BaseModel) :
    refresh_token : str

class RefreshResponse(BaseModel) :
    access_token : str
    token_type : str

class LogoutRequest(BaseModel) :
    refresh_token : str