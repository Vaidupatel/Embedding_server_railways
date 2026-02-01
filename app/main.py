from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from app.auth import verify_bearer
from app.embedding import embed_texts
from app.config import MAX_CHUNKS

app = FastAPI(title="Embedding Service", version="1.0")

class EmbedRequest(BaseModel):
    texts: list[str]
    normalize: bool = True

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/embed")
def embed(req: EmbedRequest, _=Depends(verify_bearer)):
    if not req.texts:
        raise HTTPException(status_code=400, detail="No texts provided")

    if len(req.texts) > MAX_CHUNKS:
        raise HTTPException(
            status_code=400,
            detail=f"Max {MAX_CHUNKS} chunks allowed"
        )

    embeddings = embed_texts(req.texts, req.normalize)
    return {"embeddings": embeddings}
