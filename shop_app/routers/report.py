from datetime import date
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from shop_app.crud import crud_purchase, crud_product
from fastapi import Request, Depends
from shop_app.user_authentication import templates, get_current_active_user, get_db
from fastapi import APIRouter, Form


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/purchase/report", response_class=HTMLResponse)
async def purchase_list(request: Request, db: Session = Depends(get_db)):
    purchase_items = crud_purchase.get_all_purchase(db)
    return templates.TemplateResponse("purchase_report.html", {"request": request, "purchase_items": purchase_items})


@router.get("/sales/report", response_class=HTMLResponse)
async def purchase_list(request: Request):
    return templates.TemplateResponse("sales_report.html", {"request": request})
