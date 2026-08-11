from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.permissions import require_admin
from app.database.database import get_db
from app.schemas.user import UserCreate
from app.services.auth_service import auth_service
from app.services.jwt_service import jwt_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# --- REGISTER ROUTES ---


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    """Renders the sign-up page."""
    return templates.TemplateResponse(
        request=request, name="register.html", context={"request": request}
    )


@router.post("/register")
def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Handles user registration and redirects to login on success."""
    user_data = UserCreate(
        username=username,
        email=email,
        password=password,
    )

    try:
        user = auth_service.register_user(db, user_data)
    except ValueError as e:
        return {"error": str(e)}

    return RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER,
    )


# --- LOGIN ROUTES ---


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Renders the login page."""
    return templates.TemplateResponse(
        request=request, name="login.html", context={"request": request}
    )

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user=Depends(get_current_user)):
    """Renders user dashboard."""
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request, "user": user},
    )
@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Authenticates user and redirects based on role (Admin -> /admin/products, User -> /products)."""
    user = auth_service.authenticate_user(db, email, password)

    if not user:
        return {"error": "Invalid credentials"}

    token = jwt_service.create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
        }
    )

    # Check user role for dynamic redirection
    redirect_url = (
        "/admin/dashboard"
        if getattr(user, "role", "").lower() == "admin"
        else "/dashboard"
    )

    response = RedirectResponse(
        url=redirect_url,
        status_code=status.HTTP_303_SEE_OTHER,
    )

    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
    )

    return response

# --- LOGOUT & USER INFO ROUTES ---


@router.get("/logout")
def logout():
    """Clears authentication token cookie and redirects to login page."""
    response = RedirectResponse(
        url="/login",
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.delete_cookie("token")
    return response


@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    """Returns current authenticated user details in JSON format."""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }





@router.get("/admin")
def admin_dashboard(admin=Depends(require_admin)):
    """Admin-only protected endpoint."""
    return {"message": f"Welcome Admin {admin.username}"}