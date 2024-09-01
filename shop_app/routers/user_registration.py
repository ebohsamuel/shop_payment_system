from fastapi.responses import HTMLResponse
from shop_app.schemas import schemas_user
from shop_app.crud import crud_user
from fastapi import Request, Depends, HTTPException
from shop_app.user_authentication import get_db
from shop_app.user_authentication import templates, create_access_token, check_admin
from fastapi import APIRouter, Form
from sqlalchemy.orm import Session
from mailjet_rest import Client


MAILJET_API_KEY = '19e4793771daf163d05fad4d190cf244'
MAILJET_SECRET_KEY = 'd9f2c1198b71e4e6b7ce9e0a315bdbe3'

mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')

router = APIRouter(dependencies=[Depends(check_admin)])


@router.get("/user/enter-new-user", response_class=HTMLResponse)
async def new_user_form(request: Request):
    return templates.TemplateResponse("new-user-form.html", {"request": request})


@router.post("/user/enter-new-user", response_class=HTMLResponse)
async def enter_new_user(
        request: Request,
        email: str = Form(),
        password: str = Form(),
        fullname: str = Form(),
        is_admin: bool | None = Form(default=None),
        db: Session = Depends(get_db),
):
    if not is_admin:
        is_admin = False
    user_token = create_access_token(data={"sub": email})

    activation_link = f"http://127.0.0.1:8000/activate/{user_token}"

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "osadebamwencharles007@gmail.com",  # Sender's email
                    "Name": "Esert Ltd"
                },
                "To": [
                    {
                        "Email": email,  # Recipient's email
                        "Name": fullname
                    }
                ],
                "Subject": "Activate your account",
                "TextPart": "Please activate your account.",
                "HTMLPart": f"""
                <h3>Welcome to Esert Ltd!</h3>
                <p>Dear User,</p>
                
                <p>Thank you for registering with Esert Ltd. To complete your registration and activate your account, please click the link below:</p>
                
                <p><a href='{activation_link}' style='color: #1a73e8; text-decoration: none; font-weight: bold;'>Activate Your Account</a></p>
                
                <p>If you did not create an account with us, please disregard this email.</p>
                
                <p>Best regards,<br>
                The Esert Ltd Team</p>
"""
            }
        ]
    }
    result = mailjet.send.create(data=data)

    if result.status_code == 200:
        user_data = schemas_user.UserCreate(email=email, password=password, fullname=fullname, is_admin=is_admin)
        db_user = crud_user.create_user(db=db, user_data=user_data)
        return templates.TemplateResponse("new-user-form.html", {"request": request})
    else:
        raise HTTPException(status_code=500, detail="Failed to register user")
