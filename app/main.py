from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List

from app.security import verify_bearer_token
from app.embedding import embed_texts
from app.config import MAX_CHUNKS, MODEL_NAME

app = FastAPI(title="Embedding Service", version="1.0.0")


class EmbedRequest(BaseModel):
    texts: List[str]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_NAME
    }


@app.post("/embed", dependencies=[Depends(verify_bearer_token)])
def embed(req: EmbedRequest):
    texts = req.texts

    if not texts:
        raise HTTPException(status_code=400, detail="No texts provided")

    if len(texts) > MAX_CHUNKS:
        raise HTTPException(
            status_code=400,
            detail=f"Max {MAX_CHUNKS} texts allowed per request"
        )

    for t in texts:
        if not isinstance(t, str) or not t.strip():
            raise HTTPException(status_code=400, detail="Invalid text input")

    embeddings = embed_texts(texts)

    return {
        "count": len(embeddings),
        "embeddings": embeddings
    }
