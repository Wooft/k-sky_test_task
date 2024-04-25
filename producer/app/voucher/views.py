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