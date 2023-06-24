FROM python:3.10-bookworm

WORKDIR /app
COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
