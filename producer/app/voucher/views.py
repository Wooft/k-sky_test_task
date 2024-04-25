from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .kafka_producer import send_to_kafka
from .models import Voucher, Product, ProductVoucher
from .serializers import VoucherCreateSeriazlizer, VoucherSerializer

class ChecksViewSet(ModelViewSet):
    serializer_class = VoucherCreateSeriazlizer
    queryset = Voucher.objects.all()
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        """
        Создает чек и связанные с ним товары на основе данных запроса.

        Принимает POST-запрос с данными чека и списком товаров. Сначала проверяет,
        предоставлен ли список товаров 'items'. Если список не предоставлен, возвращает
        ответ с ошибкой 400. Далее происходит валидация данных чека. Если данные валидны,
        создает чек и связанные с ним товары, сохраняет их в базе данных и отправляет
        информацию в Kafka. В случае успеха возвращает сериализованные данные ваучера
        и статус 201. Если данные невалидны, возвращает ошибки валидации и статус 400.

        Параметры:
            request: HttpRequest - HTTP запрос, содержащий данные чека и товаров.

        Возвращает:
            Response: HttpResponse - ответ с сериализованными данными ваучера и статусом 201
                      в случае успешного создания или с ошибками валидации и статусом 400.
        """
        items = request.data.pop('items', None)
        if not items:
            return Response({'detail': 'No items provided.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = VoucherCreateSeriazlizer(data=request.data)
        if serializer.is_valid():
            voucher = Voucher.objects.create(**serializer.validated_data)
            for item in items:
                quantity = item.pop('quantity', None)
                product = Product.objects.get_or_create(**item)[0]
                ProductVoucher(product=product, voucher=voucher, quantity=quantity).save()
            result = VoucherSerializer(voucher).data
            for product in result['items']:
                product['quantity'] = ProductVoucher.objects.filter(product=product['product_id'], voucher=voucher.transaction_id).first().quantity
            send_to_kafka(data=result)
            return Response(data=result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)