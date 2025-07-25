FROM python:3.10

RUN apt-get update && apt-get install -y libglib2.0-0 libgl1-mesa-glx

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]