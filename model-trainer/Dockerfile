FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY run.sh ./
RUN chmod +x ./run.sh
CMD ./run.sh $train_file_location $train_file_name $ml_user