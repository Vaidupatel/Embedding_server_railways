import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

MODEL_DIR = "/models/bge-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

session = ort.InferenceSession(
    f"{MODEL_DIR}/model.onnx",
    providers=["CPUExecutionProvider"]
)

def l2_normalize(v):
    norm = np.linalg.norm(v)
    return v if norm == 0 else v / norm

def embed_texts(texts, normalize=True):
    results = []

    for text in texts:
        inputs = tokenizer(
            text,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="np"
        )

        ort_inputs = {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
        }

        embedding = session.run(None, ort_inputs)[0][0]

        if normalize:
            embedding = l2_normalize(embedding)

        results.append(embedding.tolist())

    return results
