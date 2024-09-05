from paystackapi.paystack import Paystack
from fastapi import APIRouter, HTTPException
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
import json
from starlette.responses import JSONResponse
from shop_app.schemas import schemas_sales, schemas_user
from shop_app.user_authentication import get_current_user, templates, get_db
from shop_app.crud import crud_product_category, crud_product, crud_sales
from sqlalchemy.orm import Session
from shop_app.utility import sales_dashboard


paystack = Paystack(secret_key="sk_test_3fe28fa52c4d4e9335025c446fcf47f14d5c14d5")

router = APIRouter()


@router.get("/sales/payment/paystack")
async def paystack_payment(request: Request):
    total_amount = int(request.query_params.getlist("amount")[0])
    email = request.query_params.getlist("email")[0]

    amount = total_amount * 100
    response_ = paystack.transaction.initialize(email=email, amount=amount)

    if not response_['status']:
        return HTMLResponse(content="""
                   <h1>Payment Not Successful</h1>
                   <p>It seems that the payment initialization has failed.</p>
                   <p>Please try again or contact customer support if the issue persists.</p>
                   <a href="/sales/sales-platform" class="button">Return to Sales Page</a>
               """, status_code=400)

    response = RedirectResponse(response_['data']['authorization_url'])

    return response


@router.get("/payment/callback")
async def payment_callback(
        request: Request,
        user: schemas_user.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    payment_reference = request.query_params.get("reference")
    response_ = paystack.transaction.verify(payment_reference)
    if not response_['status']:
        return HTMLResponse(content="""
            <h1>Payment Not Successful</h1>
            <p>It seems that the payment transaction has failed.</p>
            <p>Please try again or contact customer support if the issue persists.</p>
            <a href="/sales/sales-platform" class="button">Return to Sales Page</a>
        """, status_code=400)

    items_sold = request.cookies.get("sales_items")
    if not items_sold:
        return templates.TemplateResponse("expired_sales_process.html", {"request": request})

    items_sold = json.loads(items_sold)

    # customer_name = response_['data']['customer']['first_name'] + ' ' + response_['data']['customer']['last_name']
    total_amount = response_['data']['amount'] * 0.01
    customer_email = response_['data']['customer']['email']

    order_details = {
        "user_id": user.id,
        "total_amount": total_amount,
        "customer_email": customer_email,
        "payment_method": 'paystack'
    }
    return JSONResponse(content=order_details)

"""
    order_details = schemas_sales.OrderCreate(
        user_id=user.id,
        total_amount= total_amount,
        customer_name=customer_name,
        customer_email=customer_email,
        payment_method='paystack'
    )
    db_product = None
    db_order_item = None

    db_order = crud_sales.create_new_order(db, order_details)

    for item in items_sold.get("processedItems"):
        db_product = crud_product.get_product_by_product_name(db=db, product_name=item.get("product_name"))
        order_item_details = schemas_sales.OrderItemCreate(
            order_id=db_order.id,
            product_id=db_product.id,
            product_category_id=db_product.product_category_id,
            quantity=item.get("quantity"),
            sales_price=item.get("price")
        )
        # create the order item
        db_order_item = crud_sales.create_new_order_item(db, order_item_details)

        # adjust stock in the product table
        db_product.stock -= item.get("quantity")
    db.commit()
    if db_product:
        db.refresh(db_product)
    if db_order_item:
        db.refresh(db_order_item)

    products_category = crud_product_category.get_all_product_category(db)
    rendered_products_category = sales_dashboard(products_category)
    return templates.TemplateResponse(
        "product_category_directory_for_sales.html", {"request": request, "products": rendered_products_category})
"""



