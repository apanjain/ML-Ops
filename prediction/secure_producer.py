from confluent_kafka import Producer
import os
import json

from dotenv import load_dotenv

DEBUG = os.environ.get('MODE', 'DEV') != 'PROD'

if DEBUG:
    load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.environ.get(
    'KAFKA_BOOTSTRAP_SERVERS', '0.0.0.0:9092')
KAFKA_USER = os.environ.get('KAFKA_USER', '')
KAFKA_PASS = os.environ.get('KAFKA_PASS', '')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', '')
CA_CERT_LOCATION = os.environ.get('CA_CERT_LOCATION', '/key-used/ca-cert')
ML_USERNAME = os.environ.get('ML_USERNAME', 'root')
TRAIN_FILE_LOCATION = os.environ.get('TRAIN_FILE_LOCATION', 'uploads/train.py')

# print(ML_USERNAME)


def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed :{str(err)}")
    else:
        print(
            f"Message is delivered to the partition {msg.partition()}; Offset -{msg.offset()}")
        print(f"msg_sent is : {msg.value().decode('utf-8')}")


def run_producer(msg_value):
    p = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
                  'security.protocol': 'sasl_ssl',
                  'sasl.mechanism': 'SCRAM-SHA-512',
                  'sasl.username': KAFKA_USER,
                  'sasl.password': KAFKA_PASS,
                  'ssl.ca.location': CA_CERT_LOCATION,
                  'acks': '-1',  # all
                  'partitioner': 'consistent_random'})

    msg_header = {"source": b"check"}
    try:
        p.poll(timeout=0)
        p.produce(topic=KAFKA_TOPIC, value=json.dumps(msg_value).encode("utf-8"),
                  headers=msg_header, on_delivery=delivery_report)
    except BufferError as buffer_error:
        print(
            f"{buffer_error} ::Waiting until the Queue gets some free space.")
    p.flush()


if __name__ == '__main__':
    message = {"train_file_location": ".", "train_file_name": TRAIN_FILE_LOCATION,
               "ml_username": ML_USERNAME, }
    run_producer(message)
