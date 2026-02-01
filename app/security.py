from fastapi import Header, HTTPException
from app.config import AUTH_TOKEN

def verify_bearer_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid bearer token")
