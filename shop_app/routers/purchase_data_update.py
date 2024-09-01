from datetime import date
from fastapi.responses import HTMLResponse
from shop_app.crud import crud_purchase, crud_product
from fastapi import Request, Depends
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, check_admin
from fastapi import APIRouter, Form
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(check_admin)])


@router.get("/purchase/purchase-data", response_class=HTMLResponse)
async def purchase_list(request: Request):
    return templates.TemplateResponse("purchase_list.html", {"request": request})


@router.get(
    "/purchase/{product_name}/{purchase_id}/update",
    response_class=HTMLResponse,
)
async def update_purchase_form(
        request: Request,
        purchase_id: int,
        product_name: str
):
    return templates.TemplateResponse(
        "update_purchase_form.html",
        {"request": request, "purchase_id": purchase_id, "product_name": product_name}
    )


@router.post(
    "/purchase/purchase-data",
    response_class=HTMLResponse,
)
async def submit_purchase_update(
        request: Request,
        product_name: str,
        purchase_id: int,
        date_purchased: date | None = Form(default=None),
        quantity: int | None = Form(default=None),
        per_cost: float | None = Form(default=None),
        total_cost: float | None = Form(default=None),
        db: Session = Depends(get_db),
):
    if quantity:
        db_product = crud_product.get_product_by_product_name(db, product_name)
        db_purchase = crud_purchase.get_purchase_by_id(db, purchase_id)
        db_product.stock = db_product.stock - db_purchase.Quantity + quantity
        db.commit()
        db.refresh(db_product)

    purchase_details = {
        "date_purchased": date_purchased,
        "Quantity": quantity,
        "per_cost": per_cost,
        "total_cost": total_cost
    }
    db_purchase = crud_purchase.update_purchase(db,purchase_details,purchase_id)
    return templates.TemplateResponse("purchase_list.html", {"request": request})
