FROM python:3.10.8-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /api
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
