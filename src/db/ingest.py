import os
from dotenv import load_dotenv
from src.db.vector_store import get_vector_store
from langchain_text_splitters import RecursiveCharacterTextSplitter
import glob
from langchain_community.document_loaders import PyPDFLoader, BSHTMLLoader

def ingest_documents(data_dir: str = "data"):
    load_dotenv()
    store = get_vector_store()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    files = glob.glob(f"{data_dir}/*.pdf") + glob.glob(f"{data_dir}/*.htm*")
        
    if not files:
        print(f"No documents found in ./{data_dir}/. Please drop a 10-K PDF or HTML file in there.")
        return

    for file_path in files:
        print(f"\nProcessing: {file_path}")
        
# Route to the correct loader based on extension
        if file_path.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        else:
            try:
                # Try standard UTF-8 encoding first
                loader = BSHTMLLoader(file_path, open_encoding="utf-8")
                documents = loader.load()
            except Exception:
                # If it hits a Microsoft smart quote (0x92), fall back to Windows-1252
                loader = BSHTMLLoader(file_path, open_encoding="windows-1252")
                documents = loader.load()
                
        chunks = text_splitter.split_documents(documents)
        print(f"Generated {len(chunks)} chunks. Writing to PostgreSQL...")
        
        store.add_documents(chunks)
        print(f"Successfully ingested {file_path}")

if __name__ == '__main__':
    os.makedirs("data", exist_ok=True)
    ingest_documents()