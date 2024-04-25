from django.db import models
import uuid

class Product(models.Model):
    product_id = models.PositiveIntegerField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)


class Voucher(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    items = models.ManyToManyField(Product, through='ProductVoucher')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    nds_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tips_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=100)
    place = models.CharField(max_length=250)


class ProductVoucher(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productvoucher')
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='productvoucher')
    quantity = models.PositiveIntegerField()