FROM alpine:3.11

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pio3 --no-cache-dir install -r requirements.txt

CMD ["python3","src/App.py"]