FROM python:3.11.1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt