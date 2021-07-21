# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# environment variables
ENV APP_HOME=/app \
    PYTHONUNBUFFERED=1 \
    MODE=PROD

WORKDIR $APP_HOME

# Install libredkafka
RUN apt-get update
RUN apt-get install librdkafka-dev -y
# Install production dependencies.
RUN pip install kubernetes pytz confluent-kafka

# Copy local code to the container image.
COPY . ./

CMD python app.py