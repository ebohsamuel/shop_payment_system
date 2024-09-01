from datetime import date
from fastapi.responses import HTMLResponse
from shop_app.schemas import schemas_purchase, schemas_product
from shop_app.crud import crud_purchase, crud_product_category, crud_product
from fastapi import Request, Depends
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, check_admin
from fastapi import APIRouter, Form
from sqlalchemy.orm import Session
from base64 import b64encode

router = APIRouter(dependencies=[Depends(check_admin)])


@router.get("/purchase/product-category", response_class=HTMLResponse)
async def get_product_category(request: Request, db: Session = Depends(get_db)):
    products_category = crud_product_category.get_all_product_category(db)
    rendered_products_category = []
    for product in products_category:
        # Encode the image data to a Base64 string
        image_data_base64 = b64encode(product.image_data).decode()
        rendered_products_category.append({
            "product_name": product.product_name,
            "image_data": image_data_base64,
            "product_category_id": product.id
        })

    return templates.TemplateResponse(
        "product_category_directory_for_purchase.html", {"request": request, "products": rendered_products_category})


@router.get("/purchase/{product_name}/{product_category_id}", response_class=HTMLResponse)
async def new_purchase_form(
        request: Request,
        product_name: str,
        product_category_id: int
):
    return templates.TemplateResponse(
        "new-purchase-form.html",
        {
            "request": request,
            "product_name": product_name,
            "product_category_id": product_category_id
        }
    )


@router.post("/purchase/add", response_class=HTMLResponse)
async def enter_new_product_category(
        request: Request,
        product_category_id: int = Form(),
        date_purchased: date = Form(),
        product_name: str = Form(),
        quantity: int = Form(),
        per_cost: float = Form(),
        total_cost: float = Form(),
        db: Session = Depends(get_db),
):

    purchase = schemas_purchase.PurchaseCreate(
        date_purchased=date_purchased,
        product_name=product_name,
        product_category_id=product_category_id,
        Quantity=quantity,
        per_cost=per_cost,
        total_cost=total_cost
    )
    db_purchase = crud_purchase.add_new_purchase(db, purchase)

    # we are going to use this same endpoint to update our stock in the product table
    db_product = crud_product.get_product_by_product_name(db, product_name)
    if db_product:
        db_product.stock += quantity
        db.commit()
        db.refresh(db_product)
    else:
        product = schemas_product.ProductCreate(
            product_name=product_name,
            product_category_id=product_category_id,
            stock=quantity
        )
        db_product = crud_product.add_new_product(db, product)

    return templates.TemplateResponse(
        "new-purchase-form.html",
        {
            "request": request,
            "product_name": product_name,
            "product_category_id": product_category_id
        }
    )
