from kafka import KafkaConsumer
from decouple import config
import json
from pprint import pprint
from analytics.models import Place, Receipt, Category, Product, ProductReceipt


def start_consumer():
    """
    Запускает потребителя Kafka для обработки и записи входящих сообщений в базу данных.

    Функция инициализирует потребителя Kafka с конфигурацией, заданной через переменные окружения.
    Потребитель подписывается на топик Kafka, указанный в конфигурации, и слушает новые сообщения.
    Каждое полученное сообщение обрабатывается: извлекаются данные о месте продажи, квитанции и продуктах.
    На их основе создаются или обновляются записи в базе данных для соответствующих моделей Place, Receipt и Product.

    Данные из сообщения десериализуются и используются для создания или обновления записей в базе данных,
    включая связывание продуктов с квитанциями и категориями. Если записи для указанных данных уже существуют,
    они не будут созданы заново, а будут использоваться текущие экземпляры.

    Этот процесс выполняется в бесконечном цикле для непрерывной обработки входящих сообщений.
    """
    consumer = KafkaConsumer(
        config('KAFKA_TOPIC'),
        bootstrap_servers=[f'{config("KAFKA_HOST")}:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        data = message.value
        place = Place.objects.get_or_create(place_name=data['place'])[0]
        receipt = Receipt.objects.get_or_create(transaction_id=data['transaction_id'],
                                                place=place,
                                                payment_method=data['payment_method'],
                                                total_amount=data['total_amount'],
                                                nds_amount=data['nds_amount'],
                                                tips_amount=data['tips_amount'])[0]
        for item in data['items']:
            category = Category.objects.get_or_create(name=item['category'])[0]
            product = Product.objects.get_or_create(product_id=item['product_id'],
                                                    price=item['price'],
                                                    category=category)[0]
            ProductReceipt(product=product,
                           receipt=receipt,
                           quantity=item['quantity']).save()


if __name__ == "__main__":
    start_consumer()
