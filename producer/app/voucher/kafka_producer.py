from kafka import KafkaProducer
from decouple import config
import json


def send_to_kafka(data):
    """
    Отправляет данные в Kafka топик.

    Функция инициализирует KafkaProducer с указанием сервера брокера Kafka
    и сериализатора для сообщений. Отправляет данные в топик, определенный в
    конфигурации. После отправки данных выполняет flush, чтобы убедиться, что все
    асинхронные сообщения были отправлены.

    Параметры:
        data: dict - Словарь с данными, которые будут отправлены в Kafka.

    Возвращаемое значение отсутствует.
    """
    producer = KafkaProducer(bootstrap_servers=[f'{config("KAFKA_HOST")}:9092'],  # Адрес Kafka брокера
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))  # Сериализация сообщений в JSON)
    producer.send(config('KAFKA_TOPIC'), data)
    producer.flush()

