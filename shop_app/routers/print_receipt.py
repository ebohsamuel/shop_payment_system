from fastapi.responses import HTMLResponse
from shop_app.crud import crud_sales
from fastapi import Request, Depends, Response
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, get_current_active_user
from fastapi import APIRouter
from sqlalchemy.orm import Session
import pdfkit

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/print/{order_id}")
async  def printing(
        request: Request,
        order_id: int,
        db: Session = Depends(get_db)
):
    order = crud_sales.get_order_by_id(db, order_id)
    order_items = order.orderitems

    total_amount = f"₦ {order.total_amount:,}"

    html_content = templates.get_template("print.html").render(
        order_items=order_items, total_amount=total_amount, request=request,
        order=order
    )

    pdf = pdfkit.from_string(html_content, False)
    headers = {
        'Content-Disposition': 'attachment; filename="receipt.pdf"'
    }
    return Response(content=pdf, media_type="application/pdf", headers=headers)
