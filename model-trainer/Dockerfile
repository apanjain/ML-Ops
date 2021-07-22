FROM python:3.9-slim

WORKDIR /app

COPY run.sh ./
RUN chmod +x ./run.sh
CMD ./run.sh $train_file_location $ml_user