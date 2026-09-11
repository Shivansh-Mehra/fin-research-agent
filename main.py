from dotenv import load_dotenv
import os

load_dotenv()  

def main():
    print("Initializing Multi-Agent Financial Researcher...")

    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY is not set in the environment variables.")
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY is not set in the environment variables.")

    print(f"Loaded LLM: {os.getenv('GROQ_MODEL')}")
    print(f"Loaded Embedding Model: {os.getenv('EMBEDDING_MODEL')}")
    print("Ready to compile Graph.")

if __name__ == "__main__":
    main()