from fastapi.responses import HTMLResponse
from shop_app.crud import crud_user
from fastapi import Depends, HTTPException, status
from shop_app.user_authentication import get_db, InvalidTokenError
from shop_app.user_authentication import jwt, SECRET_KEY, ALGORITHM
from fastapi import APIRouter
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/activate/{token}")
async def activate_user(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    db_user = crud_user.get_user_by_email(db, email)
    if not db_user:
        raise credentials_exception
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return {"message": "User activated successfully!"}
