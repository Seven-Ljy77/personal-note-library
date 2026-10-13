from pwdlib import PasswordHash
from dotenv import load_dotenv
import os
from datetime import datetime , timezone , timedelta
import jwt
import secrets
import hashlib

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
REFRESH_TOKEN_EXPIRE_HOURS = int(os.environ["REFRESH_TOKEN_EXPIRE_HOURS"])
ACCESS_TOKEN_SECRET_KEY = os.environ["ACCESS_TOKEN_SECRET_KEY"]
ALGORITHM = "HS256"


password_hash = PasswordHash.recommended()

def create_accesstoken(id : int) -> str :
    expire_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub" : str(id),
        "exp" : expire_at
    }
    return jwt.encode(
        payload , 
        ACCESS_TOKEN_SECRET_KEY,
        algorithm=ALGORITHM
    )

def create_refreshtoken() -> str :
    return secrets.token_hex(32)

def hash_refresh_token(refresh_token : str) -> str :
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()

def cal_refreshtoken_expire_at() -> datetime : 
    return datetime.now(timezone.utc) + timedelta(
        hours=REFRESH_TOKEN_EXPIRE_HOURS
    )