from fastapi import Header, HTTPException
from app.config import API_TOKEN

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.split("Bearer ")[1]
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
