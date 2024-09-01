from fastapi.responses import RedirectResponse
from fastapi import APIRouter, status

router = APIRouter()


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token", httponly=True)
    return response
