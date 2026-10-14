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

class GetUserResponse(BaseModel) :
    id : int
    username : str
    created_at : datetime
    is_active : bool
    notes_num : int

class GetNoteListResponse(BaseModel) :
    id : int
    title : str
    created_at : datetime
    update_at : datetime

class CreateNoteRequest(BaseModel) :
    title : str
    content : str

class GetNoteResponse(BaseModel) :
    id : int
    title : str
    content : str
    created_at : datetime
    updated_at : datetime

class PatchNoteRequest(BaseModel) :
    title : str | None
    content : str | None