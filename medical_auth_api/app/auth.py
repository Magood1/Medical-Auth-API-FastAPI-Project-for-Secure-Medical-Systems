from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake_user_db = {"admin@example.com": {"email": "admin@example.com", "hashed_password": pwd_context.hash("admin")}}

class User(BaseModel):
    email: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
def login(user: User, response: Response):
    db_user = fake_user_db.get(user.email)
    if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    access_token = create_access_token(data={"sub": user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"msg": "Login successful"}

@router.post("/register")
def register(user: User):
    if user.email in fake_user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = pwd_context.hash(user.password)
    fake_user_db[user.email] = {"email": user.email, "hashed_password": hashed}
    return {"msg": "User registered successfully"}