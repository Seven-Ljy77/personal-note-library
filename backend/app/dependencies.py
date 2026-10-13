from app.models import User
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from fastapi import Depends , HTTPException , status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
import jwt
from jwt.exceptions import InvalidTokenError
from app.security import ALGORITHM , ACCESS_TOKEN_SECRET_KEY
from app.models import User


def get_current_user(
    credentials : HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db : Session = Depends(get_db)
) -> User :
    try :
        data = jwt.decode(
            credentials.credentials , 
            ACCESS_TOKEN_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        id = data.get("sub")
        if id is None :
            raise ValueError

        id = int(id)

        user = db.execute(
            select(User).where(User.id == id)
        ).scalar_one_or_none()

        if user is None or not user.is_active :
            raise ValueError()

        return user
        
    except (ValueError , InvalidTokenError , TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid accesstoken",
            headers={
                "WWW-Authenticate" : "Bearer"
            }
        )