from fastapi.responses import HTMLResponse
from shop_app.crud import crud_sales
from fastapi import Request, Depends
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, get_current_active_user
from fastapi import APIRouter
from sqlalchemy.orm import Session

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/order/report", response_class=HTMLResponse)
async def order_report(
        request: Request,
        db: Session = Depends(get_db)
):
    db_orders = crud_sales.get_all_oder(db)
    for order in db_orders:
        order.created_at = order.created_at.replace(microsecond=0)
    return templates.TemplateResponse(
        "order-report.html", {"request": request, "db_orders": db_orders})


@router.get("/order/order-items/{order_id}", response_class=HTMLResponse)
async def expense_update_page(
        order_id: int,
        request: Request,
        db: Session = Depends(get_db)
):
    order = crud_sales.get_order_by_id(db, order_id)
    order_items = order.orderitems
    return templates.TemplateResponse(
        "customer-order.html",
        {"request": request, "order_items": order_items, "order": order}
    )
