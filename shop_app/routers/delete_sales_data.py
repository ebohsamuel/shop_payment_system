from fastapi.responses import HTMLResponse
from shop_app.crud import crud_product, crud_sales
from fastapi import Request, Depends
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, check_admin
from fastapi import APIRouter, Form
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(check_admin)])


@router.get("/sales/report/delete", response_class=HTMLResponse)
async def sales_report(
        request: Request,
        db: Session = Depends(get_db)
):
    db_order_items = crud_sales.get_all_order_item(db)
    for order_item in db_order_items:
        order_item.created_at = order_item.created_at.replace(microsecond=0)
    return templates.TemplateResponse(
        "sales-report-delete.html", {"request": request, "order_items": db_order_items})


@router.get(
    "/sales/delete/{order_item_id}", response_class=HTMLResponse)
async def update_sales_quantity_form(
        request: Request,
        order_item_id: int,
        db: Session = Depends(get_db)
):
    db_order_item = crud_sales.get_order_item_by_id(db, order_item_id)
    db_order = db_order_item.order
    db_product = db_order_item.product

    db_order.total_amount -= db_order_item.quantity * db_order_item.sales_price
    db_product.stock += db_order_item.quantity

    db.delete(db_order_item)

    db.commit()

    db.refresh(db_product)
    db.refresh(db_order)

    db_order_items = crud_sales.get_all_order_item(db)
    for order_item in db_order_items:
        order_item.created_at = order_item.created_at.replace(microsecond=0)
    return templates.TemplateResponse(
        "sales-report-delete.html", {"request": request, "order_items": db_order_items})
