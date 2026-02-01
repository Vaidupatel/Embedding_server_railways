from fastapi import Header, HTTPException
from app.config import API_TOKEN

def verify_bearer(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.replace("Bearer ", "").strip()
    if token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
