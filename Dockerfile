FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download ONNX model directly (NO git, NO lfs)
RUN mkdir -p /models/bge-small && \
    curl -L -o /models/bge-small/model.onnx \
      https://huggingface.co/Xenova/bge-small-en-v1.5/resolve/main/model.onnx && \
    curl -L -o /models/bge-small/tokenizer.json \
      https://huggingface.co/Xenova/bge-small-en-v1.5/resolve/main/tokenizer.json && \
    curl -L -o /models/bge-small/config.json \
      https://huggingface.co/Xenova/bge-small-en-v1.5/resolve/main/config.json

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
