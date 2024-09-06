from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from shop_app.user_authentication import templates, get_current_active_user, get_db
from shop_app.crud import crud_sales
from fastapi import Response
import pdfkit
import pandas as pd
from io import BytesIO
from dateutil import parser


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/sales/pdf")
async def sales_pdf(request: Request, db: Session = Depends(get_db)):

    start = parser.parse(request.query_params.getlist("start")[0]).date()
    end = parser.parse(request.query_params.getlist("end")[0]).date()

    sales = crud_sales.get_all_order_item_between_dates(db, start=start, end=end)

    total_amount = f"₦ {sum(sale.get("amount") for sale in sales):,}"

    html_content = templates.get_template("pdf_sales.html").render(
        sales=sales, total_amount=total_amount, request=request
    )

    pdf = pdfkit.from_string(html_content, False)
    headers = {
        'Content-Disposition': 'attachment; filename="sales.pdf"'
    }
    return Response(content=pdf, media_type="application/pdf", headers=headers)


@router.get("/sales/excel")
async def sales_excel(request: Request, db: Session = Depends(get_db)):

    start = parser.parse(request.query_params.getlist("start")[0]).date()
    end = parser.parse(request.query_params.getlist("end")[0]).date()

    sales = crud_sales.get_all_order_item_between_dates(db, start, end)

    df = pd.DataFrame(sales)
    df.columns = [
            "Date",
            "Customer Name",
            "Customer Email",
            "Attendant",
            "Payment Method",
            "Product Name",
            "Quantity",
            "Sales Price",
            "Total Amount"
        ]

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    buffer.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="sales.xlsx"'
    }
    return Response(content=buffer.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)


