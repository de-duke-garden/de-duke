import uvicorn
from fastapi import FastAPI
import sentence_transformers
import numpy as np
import os
import boto3
import json


# Load Hugging Face token from environment
# hf_token = os.getenv("HF_TOKEN")
try:
    HF_TOKEN_ARN = os.environ.get("HF_TOKEN_ARN")
    if HF_TOKEN_ARN:
        client = boto3.client(
            "secretsmanager", region_name=os.environ.get("AWS_REGION")
        )
        response = client.get_secret_value(SecretId=HF_TOKEN_ARN)
        secret_string = response.get("SecretString")
        secret_dict = json.loads(secret_string)
        HF_TOKEN = secret_dict.get("token")
except Exception as e:
    print(f"Error retrieving HF_TOKEN: {e}")

# Initialize model with authentication token
model = sentence_transformers.SentenceTransformer(
    "google/embeddinggemma-300m",
    token=HF_TOKEN
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
