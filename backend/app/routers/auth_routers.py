from fastapi import APIRouter , Depends , HTTPException , status , Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.schemas import RegisterRequest , RegisterResponse , LoginRequest , LoginResponse , RefreshRequest , RefreshResponse , LogoutRequest
from app.models import User , RefreshToken
from app.security import password_hash , create_accesstoken , create_refreshtoken , hash_refresh_token , cal_refreshtoken_expire_at
from datetime import datetime , timezone
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/api/auth",
    tags=["router"]
)

@router.post(
    "/register",
    response_model=RegisterResponse
)
def register(
    data : RegisterRequest,
    db : Session = Depends(get_db),
) :
    user = db.execute(
        select(User).where(User.username == data.username)
    ).scalar_one_or_none()

    if user is not None :
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT ,
            detail="Username has existed"
        )

    user = User(
        username = data.username,
        hashed_password = password_hash.hash(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    data : LoginRequest,
    db : Session = Depends(get_db)
) :
    httpexception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="username or password is wrong",
        headers={
            "WWW-Authenticate" : "Bearer"
        }
    )
    
    user = db.execute(
        select(User).where(User.username == data.username)
    ).scalar_one_or_none()

    if user is None or not password_hash.verify(data.password , user.hashed_password) or not user.is_active : 
        raise httpexception

    accesstoken = create_accesstoken(user.id)
    refreshtoken = create_refreshtoken()

    # 用于 HTTP 响应
    payload = {
        "access_token" : accesstoken,
        "refresh_token" : refreshtoken,
        "token_type" : "bearer"
    }

    # 存入 pgsql
    rt = RefreshToken(
        hashed_refreshtoken = hash_refresh_token(refreshtoken),
        user_id = user.id,
        expire_at = cal_refreshtoken_expire_at()
    )

    db.add(rt)
    db.commit()

    return payload


@router.post(
    "/refresh",
    response_model=RefreshResponse
)
def refresh(
    data : RefreshRequest,
    db : Session = Depends(get_db)
) :
    httpexception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="refresh token unvalid",
        headers={
            "WWW-Authenticate" : "Bearer"
        }
    )
    
    hashed_refresh_token = hash_refresh_token(data.refresh_token)
    
    refresh_token = db.execute(
        select(RefreshToken).where(RefreshToken.hashed_refreshtoken == hashed_refresh_token)
    ).scalar_one_or_none()

    if refresh_token is None or not refresh_token.is_active or refresh_token.expire_at <= datetime.now(timezone.utc)  :
        raise httpexception

    user = db.execute(
        select(User).where(User.id == refresh_token.user_id)
    ).scalar_one_or_none()

    if user is None or not user.is_active :
        raise httpexception

    accesstoken = create_accesstoken(refresh_token.user_id)

    payload = {
        "access_token" : accesstoken,
        "token_type" : "bearer"
    }

    return payload


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    data : LogoutRequest,
    user : User = Depends(get_current_user),
    db : Session = Depends(get_db)
) :
    httpexception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token",
        headers={
            "WWW-Authenticate" : "Bearer"
        }
    )
    
    hashed_refresh_token = hash_refresh_token(data.refresh_token)
    
    rt = db.execute(
        select(RefreshToken).where(RefreshToken.hashed_refreshtoken == hashed_refresh_token)
    ).scalar_one_or_none()

    if rt is None or rt.user_id != user.id or rt.expire_at <= datetime.now(timezone.utc) or not rt.is_active:
        raise httpexception

    rt.is_active = False
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)