from fastapi.responses import HTMLResponse
from shop_app.schemas import schema_product_category
from shop_app.crud import crud_product_category
from fastapi import Request, Depends, HTTPException
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, check_admin
from fastapi import APIRouter, Form, UploadFile, File
from sqlalchemy.orm import Session

router = APIRouter(dependencies=[Depends(check_admin)])


@router.get("/enter/product-category", response_class=HTMLResponse)
async def new_product_form(request: Request):
    return templates.TemplateResponse("new-product-category-form.html", {"request": request})


@router.post("/product-category/add", response_class=HTMLResponse)
async def enter_new_product_category(
        request: Request,
        product_name: str = Form(),
        image_data: UploadFile = File(),
        db: Session = Depends(get_db),
):
    db_product_category = crud_product_category.get_product_category_by_product_name(db, product_name)
    if db_product_category:
        return HTTPException(status_code=400, detail="Product name already exists")
    image_data = await image_data.read()
    product_category = schema_product_category.ProductCategoryCreate(
        product_name=product_name,
        image_data=image_data
    )
    db_product_category = crud_product_category.add_new_product_category(db, product_category)
    return templates.TemplateResponse("new-product-category-form.html", {"request": request})
