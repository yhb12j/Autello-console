from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.database import get_db
from core.security import create_access_token, get_current_admin, hash_password, verify_password
from models.admin import AdminCRUD
from schemas import AdminLogin, AdminOut, AdminRegister, AuthCheckOut, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/check", response_model=AuthCheckOut)
def check_admins():
    with get_db() as conn:
        return {"exists": AdminCRUD.count(conn) > 0}


@router.post("/register", response_model=AdminOut, status_code=201)
def register_admin(payload: AdminRegister):
    with get_db() as conn:
        if AdminCRUD.count(conn) > 0:
            raise HTTPException(status_code=403, detail="Registration is closed")
        if AdminCRUD.get_by_login(conn, payload.login):
            raise HTTPException(status_code=409, detail="Login already exists")
        return AdminCRUD.create(
            conn,
            {
                "login": payload.login,
                "email": str(payload.email) if payload.email else None,
                "password_hash": hash_password(payload.password),
            },
        )


def _issue_token(login: str, password: str) -> dict:
    with get_db() as conn:
        admin = AdminCRUD.get_by_login(conn, login)
    if admin is None or not verify_password(password, admin["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": create_access_token(admin["login"]), "token_type": "bearer"}


@router.post("/login", response_model=TokenOut)
def login(payload: AdminLogin):
    return _issue_token(payload.login, payload.password)


@router.post("/token", response_model=TokenOut)
def login_token(form: OAuth2PasswordRequestForm = Depends()):
    return _issue_token(form.username, form.password)


@router.get("/me", response_model=AdminOut)
def read_me(admin: dict = Depends(get_current_admin)):
    return admin


@router.get("/verify")
def verify_token(admin: dict = Depends(get_current_admin)):
    return {"valid": True, "login": admin["login"]}
