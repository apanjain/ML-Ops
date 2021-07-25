import os
import json
from kubernetes import config
from confluent_kafka import Consumer
import job_crud
import logging

logging.basicConfig(filename='/mnt/c/pykube-debug.log', level=logging.INFO)

# Variable to decide which kubernetes configuration to load (local or incluster)
DEBUG = not (os.environ.get('MODE', 'DEV') == 'PROD')
# String of comma separated server addresses
KAFKA_BOOTSTRAP_SERVERS = os.environ.get(
    'KAFKA_BOOTSTRAP_SERVERS', '0.0.0.0:9092')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'test-topic')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', 'test-group')
KAFKA_USER = os.environ.get('KAFKA_USER', '')
KAFKA_PASS = os.environ.get('KAFKA_PASS', '')
CA_CERT_LOCATION = '/key-used/ca-cert'


def not_found():
    logging.warning("Please provide a valid input\n")


def main():
    try:
        # print(DEBUG)
        if DEBUG:
            config.load_kube_config()
        else:
            config.load_incluster_config()

        consumer = Consumer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'security.protocol': 'sasl_ssl',
            'sasl.mechanism': 'SCRAM-SHA-512',
            'sasl.username': KAFKA_USER,
            'sasl.password': KAFKA_PASS,
            'auto.offset.reset': "earliest",
            'group.id': KAFKA_GROUP_ID,
            'ssl.ca.location': CA_CERT_LOCATION})

        consumer.subscribe([KAFKA_TOPIC])
        logging.info("Starting the consumer...")

        while True:
            msg = consumer.poll(1.0)

            try:
                if msg is None:
                    continue
                if msg.error():
                    logging.error("Consumer error: {}".format(msg.error()))
                    continue
                message = json.loads(msg.value().decode("utf-8"))
                logging.info(json.dumps(message))
                train_file_location = message.get(
                    'train_file_location', '')
                train_file_name = message.get('train_file_name', 'train.py')
                ml_username = message.get('ml_username', 'root')
                job_crud.create(
                    train_file_location=train_file_location, train_file_name=train_file_name, user=ml_username)
            except Exception as e:
                logging.error(str(e))
    except Exception as e:
        logging.error(str(e))


if __name__ == "__main__":
    main()
