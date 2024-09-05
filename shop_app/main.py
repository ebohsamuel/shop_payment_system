from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from shop_app.user_authentication import templates
from fastapi import Request
from shop_app.routers import user_registration, user_activation, welcome, login, logout, user_data_update
from shop_app.routers import register_new_product_category, product_category_data_update
from shop_app.routers import enter_new_purchase, purchase_data_update, update_product_price, report
from shop_app.routers import enter_new_sales, sales_data_update, delete_sales_data, paystack_payment
from fastapi.responses import RedirectResponse
from shop_app import websocket_


app = FastAPI()

app.mount("/static", StaticFiles(directory="shop_app/static"), name="static")


app.include_router(user_registration.router)
app.include_router(user_activation.router)
app.include_router(welcome.router)
app.include_router(login.router)
app.include_router(logout.router)
app.include_router(user_data_update.router)
app.include_router(register_new_product_category.router)
app.include_router(product_category_data_update.router)
app.include_router(enter_new_purchase.router)
app.include_router(purchase_data_update.router)
app.include_router(update_product_price.router)
app.include_router(enter_new_sales.router)
app.include_router(sales_data_update.router)
app.include_router(delete_sales_data.router)
app.include_router(paystack_payment.router)
app.include_router(report.router)
app.include_router(websocket_.router)


@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

"""
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401 and "expired" in exc.detail.lower():
        # Redirect to the login page if the token has expired
        return RedirectResponse(url="/")
    else:
        # Handle other 401 unauthorized errors or re-raise the exception
        return RedirectResponse(url="/")
"""