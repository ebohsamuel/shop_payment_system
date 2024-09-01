from datetime import date
from fastapi.responses import HTMLResponse
from shop_app.crud import crud_purchase, crud_product
from fastapi import Request, Depends
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, check_admin
from fastapi import APIRouter, Form
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(check_admin)])


@router.get("/product/price-list", response_class=HTMLResponse,)
async def price_list(request: Request, db: Session = Depends(get_db)):
    products = crud_product.get_all_product(db)
    return templates.TemplateResponse("price-list.html",{"request": request, "products": products})


@router.get("/product/price/{product_name}", response_class=HTMLResponse)
async def update_price_form(
        request: Request,
        product_name: str
):
    return templates.TemplateResponse(
        "update_price_form.html",
        {"request": request, "product_name": product_name}
    )


@router.post("/product/price-list", response_class=HTMLResponse)
async def submit_price_update(
        request: Request,
        product_name: str,
        price: float | None = Form(default=None),
        db: Session = Depends(get_db),
):
    db_product = crud_product.update_product_price(db,price,product_name)
    products = crud_product.get_all_product(db)
    return templates.TemplateResponse("price-list.html", {"request": request, "products": products})
