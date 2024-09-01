from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from shop_app.user_authentication import templates, get_current_active_user

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/welcome", response_class=HTMLResponse)
async def welcome_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})
