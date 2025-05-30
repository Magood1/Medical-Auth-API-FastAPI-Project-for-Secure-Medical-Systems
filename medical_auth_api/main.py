from fastapi import FastAPI
from app import auth, protected

app = FastAPI()
app.include_router(auth.router)
app.include_router(protected.router)