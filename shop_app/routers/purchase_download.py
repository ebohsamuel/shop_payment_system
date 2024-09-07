from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request
from shop_app.user_authentication import templates, get_current_active_user, get_db
from shop_app.crud import crud_purchase
from fastapi import Response
import pdfkit
import pandas as pd
from io import BytesIO
from dateutil import parser


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/purchase/pdf")
async def sales_pdf(request: Request, db: Session = Depends(get_db)):

    start = parser.parse(request.query_params.getlist("start")[0]).date()
    end = parser.parse(request.query_params.getlist("end")[0]).date()

    purchases = crud_purchase.get_all_purchase_between_dates(db, start=start, end=end)

    total_cost = f"₦ {sum(purchase.get("total_cost") for purchase in purchases):,}"

    html_content = templates.get_template("pdf_purchase.html").render(
        purchases=purchases, total_cost=total_cost, request=request
    )

    pdf = pdfkit.from_string(html_content, False)
    headers = {
        'Content-Disposition': 'attachment; filename="purchases.pdf"'
    }
    return Response(content=pdf, media_type="application/pdf", headers=headers)


@router.get("/purchase/excel")
async def sales_excel(request: Request, db: Session = Depends(get_db)):

    start = parser.parse(request.query_params.getlist("start")[0]).date()
    end = parser.parse(request.query_params.getlist("end")[0]).date()

    purchase = crud_purchase.get_all_purchase_between_dates(db, start, end)

    df = pd.DataFrame(purchase)
    df.columns = [
            "Date of Purchase",
            "Product Name",
            "Quantity",
            "Per Cost",
            "Total Cost"
    ]

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    buffer.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="purchase.xlsx"'
    }
    return Response(content=buffer.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)


