import os
import json
from kubernetes import client, config
from confluent_kafka import Consumer
import job_crud
import deployment_crud
import logging

# logging.basicConfig(filename='/mnt/c/pykube-debug.log', level=logging.INFO)

DEBUG = not (os.environ.get('MODE', 'DEV') == 'PROD')
KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', '0.0.0.0')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'test-topic')
KAFKA_GROUP_ID = os.environ.get('KAFKA_GROUP_ID', 'test-group')
KAFKA_USER = os.environ.get('KAFKA_USER', '')
KAFKA_PASS = os.environ.get('KAFKA_PASS', '')
CA_CERT_LOCATION = os.environ.get('CA_CERT_LOCATION', '/key-used/ca-cert')


def not_found():
    logging.warning("Please provide a valid input\n")


def main():
    try:
        # print(DEBUG)
        # if DEBUG:
        #     config.load_kube_config()
        # else:
        #     config.load_incluster_config()

        switcher = {
            'create': job_crud.create,
        }

        consumer = Consumer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
            'security.protocol': 'sasl_ssl',
            'sasl.mechanism': 'SCRAM-SHA-512',
            'sasl.username': 'demo-consumer',
            'sasl.password': 'demokafka',
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
                print(message)
                # command = message.get(
                #     'command', 'invalid').lower()
                # train_file_location = message.get(
                #     'train_file_location', 'train.py')
                # model_dump_location = message.get('model_dump_location', 'tmp')
                # switcher.get(command, not_found)(
                #     train_file_location=train_file_location, model_dump_location=model_dump_location)
            except Exception as e:
                logging.error(str(e))
    except Exception as e:
        logging.error(str(e))


if __name__ == "__main__":
    main()
