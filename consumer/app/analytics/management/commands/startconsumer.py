from django.core.management.base import BaseCommand
from consumer.kafka_consumer import start_consumer


class Command(BaseCommand):
    help = 'Starts the Kafka consumer'

    def handle(self, *args, **kwargs):
        start_consumer()
