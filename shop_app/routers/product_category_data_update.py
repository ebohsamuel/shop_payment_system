from fastapi.responses import HTMLResponse
from shop_app.schemas import schema_product_category
from shop_app.crud import crud_product_category
from fastapi import Request, Depends, HTTPException
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, check_admin
from fastapi import APIRouter, Form, UploadFile, File
from sqlalchemy.orm import Session
from base64 import b64encode

router = APIRouter(dependencies=[Depends(check_admin)])


@router.get("/product_category", response_class=HTMLResponse)
async def get_products_category(request: Request, db: Session = Depends(get_db)):
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
        "product_category_directory.html", {"request": request, "products": rendered_products_category})


@router.get("/product-category/update/{product_category_id}", response_class=HTMLResponse)
async def update_product_category_form(
        request: Request,
        product_category_id: int
):
    return templates.TemplateResponse(
        "update_product_form.html",
        {"request": request, "product_category_id": product_category_id})


@router.post("/product-category", response_class=HTMLResponse)
async def submit_product_category_update(
        request: Request,
        product_category_id: int,
        product_name: str | None = Form(default=None),
        image_data: UploadFile | None = File(default=None),
        db: Session = Depends(get_db),
):
    if image_data:
        image_data = await image_data.read()

    product_category_details = {
        "product_name": product_name,
        "image_data": image_data,
    }
    db_product_category = crud_product_category.update_product_category(
        db, product_category_details, product_category_id
    )

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
        "product_category_directory.html", {"request": request, "products": rendered_products_category})
