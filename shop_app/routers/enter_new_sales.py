from datetime import date
from fastapi.responses import HTMLResponse
from shop_app.schemas import schemas_purchase, schemas_product
from shop_app.crud import crud_purchase, crud_product_category, crud_product
from fastapi import Request, Depends
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, get_current_active_user, get_current_user
from fastapi import APIRouter, Form, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from base64 import b64encode


router = APIRouter(dependencies=[Depends(get_current_active_user)])
ws_manager = crud_purchase.WebSocketManager()


@router.get("/sales/sales-platform", response_class=HTMLResponse)
async def get_product_category(request: Request, db: Session = Depends(get_db)):
    products_category = crud_product_category.get_all_product_category(db)
    rendered_products_category = []
    for product_category in products_category:
        # Encode the image data to a Base64 string
        image_data_base64 = b64encode(product_category.image_data).decode()

        if product_category.product:  # Check if there are any products in the list
            rendered_products_category.append({
                "product_name": product_category.product_name,
                "image_data": image_data_base64,
                "product_id": product_category.product[0].id  # Access the first product if it exists
            })
        else:
            # Handle the case where there are no products for the category
            rendered_products_category.append({
                "product_name": product_category.product_name,
                "image_data": image_data_base64,
                "product_id": None  # or some default value or message
            })
    return templates.TemplateResponse(
        "product_category_directory_for_sales.html", {"request": request, "products": rendered_products_category})


