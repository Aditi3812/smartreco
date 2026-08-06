from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Depends
from app.auth.dependencies import get_current_user
from fastapi.responses import RedirectResponse
router = APIRouter()
from fastapi import Form, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user import UserCreate
from app.services.auth_service import auth_service
from app.services.jwt_service import jwt_service
from app.auth.permissions import require_admin
templates = Jinja2Templates(directory="app/templates")


@router.post("/register")
def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    user_data = UserCreate(
        username=username,
        email=email,
        password=password,
    )

    try:
        user = auth_service.register_user(
            db,
            user_data,
        )

    except ValueError as e:
        return {
            "error": str(e)
        }


    return RedirectResponse(
        url="/login",
        status_code=303,
    )

@router.get(
    "/login",
    response_class=HTMLResponse,
)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )

@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    user = auth_service.authenticate_user(
        db,
        email,
        password,
    )

    if not user:
        return {
            "error": "Invalid credentials"
        }

    token = jwt_service.create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    response = RedirectResponse(
        url="/dashboard",
        status_code=303,
    )

    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
    )

    return response
@router.get("/admin")
def admin_dashboard(
    admin=Depends(require_admin),
):
    return {
        "message": f"Welcome Admin {admin.username}"
    }
@router.get("/me")
def read_me(
    current_user = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }
@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard(
    request: Request,
    user=Depends(get_current_user),
):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
        },
    )

@router.get("/logout")
def logout():

    response = RedirectResponse(
        url="/login",
        status_code=303,
    )

    response.delete_cookie("token")

    return response
