from fastapi.responses import HTMLResponse
from shop_app.crud import crud_product
from fastapi import Request, Depends
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, check_admin
from fastapi import APIRouter, Form
from sqlalchemy.orm import Session
from dateutil.parser import parse


router = APIRouter(dependencies=[Depends(check_admin)])


@router.get("/product/price-list", response_class=HTMLResponse,)
async def price_list(request: Request, db: Session = Depends(get_db)):
    products = crud_product.get_all_product(db)
    products_ = [{
        "id": product.get('id'),
        "product_name": product.get('product_name'),
        "price": product.get('price'),
        "stock": product.get('stock'),
        "product_category_id": product.get('product_category_id'),
        "created_at": parse(product.get('created_at')).replace(microsecond=0),
        "updated_at": parse(product.get('updated_at')).replace(microsecond=0)
        } for product in products]

    return templates.TemplateResponse("price-list.html",{"request": request, "products": products_})


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
