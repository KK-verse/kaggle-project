FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend app code
COPY . .

# Expose port (Cloud Run sets the PORT env variable, defaulting to 8080)
EXPOSE 8080

# Run FastAPI app with Uvicorn, mapping the host to 0.0.0.0 and port to PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
