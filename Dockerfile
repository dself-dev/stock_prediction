# Official Python base (slim for smaller size)
FROM python:3.12-slim

# Working dir in container
WORKDIR /app

# Copy/install deps first (caches better)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Fix TensorFlow warning from your logs
ENV TF_ENABLE_ONEDNN_OPTS=0

# Expose FastAPI port
EXPOSE 8000

# Run command (binds to all interfaces)
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]