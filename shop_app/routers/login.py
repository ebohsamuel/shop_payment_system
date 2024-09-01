from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta
from shop_app.user_authentication import get_db, authenticate_user, create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 660

router = APIRouter()


@router.post("/login")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url="/welcome", status_code=302)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",  # Bearer token format
        httponly=True,
    )
    return response
