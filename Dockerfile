# Use a lightweight Python 3.11 base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies required for building some Python packages
# RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install PyTorch CPU first, just like we did locally
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application code
COPY src/ ./src/
COPY main.py .
COPY ui.py .
COPY src/db/ingest.py .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI server using Uvicorn
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]