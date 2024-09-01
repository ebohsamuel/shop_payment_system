from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from shop_app.user_authentication import templates, get_db, check_admin
from shop_app.crud import crud_user

router = APIRouter(dependencies=[Depends(check_admin)])


@router.get("/user/user_list", response_class=HTMLResponse)
async def user_list(
        request: Request,
        db: Session = Depends(get_db)
):
    users = crud_user.get_users(db)
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})


@router.get("/user/update/{user_id}", response_class=HTMLResponse)
async def update_user_form(
        request: Request,
        user_id: int
):
    return templates.TemplateResponse("update_user_form.html", {"request": request, "user_id": user_id})


@router.post("/user/user_list", response_class=HTMLResponse)
async def submit_user_update(
        request: Request,
        user_id: int,
        is_active: bool | None = Form(default=None),
        fullname: str | None = Form(default=None),
        password: str | None = Form(default=None),
        email: str | None = Form(default=None),
        db: Session = Depends(get_db),
):
    if not is_active:
        is_active = False

    user_details = {
        "is_active": is_active,
        "fullname": fullname,
        "password": password,
        "email": email,
    }
    db_user = crud_user.update_user(db, user_details=user_details, user_id=user_id)
    users = crud_user.get_users(db)
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})
