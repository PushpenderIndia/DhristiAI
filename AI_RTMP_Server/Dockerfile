FROM python:3.11-slim
RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]