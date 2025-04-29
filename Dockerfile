FROM python:latest

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]