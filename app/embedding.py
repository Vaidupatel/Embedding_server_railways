import numpy as np
from transformers import AutoTokenizer
import onnxruntime as ort
from app.config import MODEL_NAME

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

session = ort.InferenceSession(
    f"https://huggingface.co/{MODEL_NAME}/resolve/main/model.onnx",
    providers=["CPUExecutionProvider"]
)

def l2_normalize(v):
    norm = np.linalg.norm(v)
    return v if norm == 0 else v / norm

def embed_texts(texts, normalize: bool = True):
    embeddings = []

    for text in texts:
        inputs = tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="np"
        )

        ort_inputs = {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"]
        }

        outputs = session.run(None, ort_inputs)
        vector = outputs[0][0]

        if normalize:
            vector = l2_normalize(vector)

        embeddings.append(vector.tolist())

    return embeddings
