from kafka import KafkaProducer
from decouple import config
import json


def send_to_kafka(data):
    producer = KafkaProducer(bootstrap_servers=[f'{config("KAFKA_HOST")}:9092'],  # Адрес Kafka брокера
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))  # Сериализация сообщений в JSON)
    producer.send(config('KAFKA_TOPIC'), data)
    producer.flush()

