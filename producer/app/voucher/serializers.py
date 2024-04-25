from rest_framework import serializers
from .models import Voucher, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class VoucherSerializer(serializers.ModelSerializer):
    items = ProductSerializer(many=True)

    class Meta:
        model = Voucher
        fields = '__all__'

class VoucherCreateSeriazlizer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ('transaction_id', 'timestamp', 'total_amount', 'nds_amount', 'tips_amount', 'payment_method', 'place')