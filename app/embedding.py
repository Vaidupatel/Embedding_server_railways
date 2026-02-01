import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer
from app.config import MODEL_DIR

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

session = ort.InferenceSession(
    f"{MODEL_DIR}/model.onnx",
    providers=["CPUExecutionProvider"]
)

def l2_normalize(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec)
    return vec if norm == 0 else vec / norm

def embed_texts(texts: list[str], normalize: bool = True) -> list[list[float]]:
    embeddings = []

    for text in texts:  # 🔒 ONE BY ONE (explicit)
        tokens = tokenizer(
            text,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="np"
        )

        outputs = session.run(
            None,
            {
                "input_ids": tokens["input_ids"],
                "attention_mask": tokens["attention_mask"],
            }
        )

        vector = outputs[0][0]

        if normalize:
            vector = l2_normalize(vector)

        embeddings.append(vector.tolist())

    return embeddings
