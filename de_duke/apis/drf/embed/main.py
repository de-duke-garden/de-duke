import uvicorn
from fastapi import FastAPI
import sentence_transformers
import numpy as np
import os


# Load Hugging Face token from environment
hf_token = os.getenv("HF_TOKEN")

# Initialize model with authentication token
model = sentence_transformers.SentenceTransformer(
    "google/embeddinggemma-300m",
    token=hf_token
)

app = FastAPI()


@app.post("/embed")
async def embed(text: str):
    # Get full 768-dimensional embedding
    tensor = model.encode_query(text)

    # Truncate to 512 dimensions (Matryoshka Representation Learning)
    truncated = tensor[:512]

    # Re-normalize the truncated embedding
    normalized = truncated / np.linalg.norm(truncated)
    return normalized.tolist()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)
