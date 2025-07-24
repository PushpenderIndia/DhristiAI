FROM python:3.11-slim

# Install FFMPEG and essential libraries for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1

WORKDIR /app

COPY requirements.txt .

# Ensure no conflicting opencv versions are present before installing
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]