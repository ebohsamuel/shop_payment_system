import json
from fastapi.responses import HTMLResponse
from shop_app.schemas import schemas_sales, schemas_user
from shop_app.crud import crud_product_category, crud_product, crud_sales
from fastapi import Request, Depends
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, get_current_active_user, get_current_user
from fastapi import APIRouter, Form, Response
from sqlalchemy.orm import Session
from shop_app.utility import sales_dashboard

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/sales/sales-platform", response_class=HTMLResponse)
async def get_product_category(request: Request, db: Session = Depends(get_db)):
    products_category = crud_product_category.get_all_product_category(db)
    rendered_products_category = sales_dashboard(products_category)
    return templates.TemplateResponse(
        "product_category_directory_for_sales.html", {"request": request, "products": rendered_products_category})


@router.get("/sales/checkout", response_class=HTMLResponse)
async def checkout_form(request: Request, db: Session = Depends(get_db)):
    product_names = request.query_params.getlist("product")
    selected_product = []
    for product_name in product_names:
        db_product = crud_product.get_product_by_product_name(db,product_name)
        selected_product.append(
            {
                "product_name": product_name,
                "price": db_product.price,
                "stock": db_product.stock,
                "id": db_product.id
            }
        )

    return templates.TemplateResponse(
        "checkout_form.html", {"request": request, "selected_product": selected_product}
    )


@router.post("/sales/set-cookies")
async def set_sales_cookies(items: schemas_sales.OrderDatas, response: Response):
    serialized_items = json.dumps(items.model_dump())
    response.set_cookie("sales_items", value=serialized_items, max_age=900, httponly=True, samesite="strict")
    print("successful")
    return {"message": "successful"}


@router.get("/sales/register-sales", response_class=HTMLResponse)
async def checkout_form(request: Request):
    total_amount = int(request.query_params.getlist("net")[0])
    return templates.TemplateResponse(
        "payment.html", {"request": request, "total_amount": total_amount}
    )


@router.post("/sales/cash-bank/add")
async def cash_back_transfer(
        request: Request,
        payment_method: str = Form(),
        customer_email: str = Form(),
        customer_name: str = Form(),
        total_amount: str = Form(),
        user: schemas_user.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    items_sold = request.cookies.get("sales_items")
    if not items_sold:
        return templates.TemplateResponse("expired_sales_process.html", {"request": request})
    items_sold = json.loads(items_sold)
    order_details = schemas_sales.OrderCreate(
        user_id=user.id,
        total_amount=total_amount,
        customer_name=customer_name,
        customer_email=customer_email,
        payment_method=payment_method
    )
    db_product = None
    db_order_item = None

    # create the new order
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


