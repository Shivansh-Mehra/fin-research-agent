import torch
import os
from langchain_postgres import PGVector
from langchain_huggingface import HuggingFaceEmbeddings

def get_vector_store():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Hardware Check: Running embeddings on {device.upper()}")

    embeddings = HuggingFaceEmbeddings(
        model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5"),
        model_kwargs={"device": device},
        encode_kwargs={"normalize_embeddings": True}
    )

    connection_string = os.getenv("DATABASE_URL")
    if not connection_string:
        raise ValueError("DATABASE_URL not found")

    vector_score = PGVector(
        embeddings=embeddings,
        collection_name="sec-filings",
        connection=connection_string,
        use_jsonb=True
    )

    return vector_score