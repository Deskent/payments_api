FROM python:3.10-slim

RUN apt-get update && \
    apt-get -y install build-essential python-dev python3-dev libgmp3-dev

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src/cryptopayment .

COPY ./tests ./tests
