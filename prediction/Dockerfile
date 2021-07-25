FROM python:3.9-slim

WORKDIR /home
ENV PYTHONUNBUFFERED=1 \
    MODE=PROD

RUN pip3 install flask gunicorn confluent-kafka python-dotenv

COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
