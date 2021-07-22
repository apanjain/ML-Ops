FROM python:3.9-slim

WORKDIR /home
ENV PYTHONUNBUFFERED=1

RUN pip3 install flask gunicorn

COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
