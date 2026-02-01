from sentence_transformers import SentenceTransformer
from app.config import MODEL_NAME

model = SentenceTransformer(MODEL_NAME)

def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = []

    for text in texts:
        emb = model.encode(
            text,
            normalize_embeddings=True  # best practice for BGE
        )
        embeddings.append(emb.tolist())

    return embeddings
