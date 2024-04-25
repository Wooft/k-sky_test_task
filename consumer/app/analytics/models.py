from django.db import models


class Place(models.Model):
    place_name = models.CharField(max_length=255)
    total_purchases = models.IntegerField(default=0)
    average_receipt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


class Taxes(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='taxes')
    total_nds = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_tips = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.PositiveIntegerField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


class Receipt(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='receipts')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    nds_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tips_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='ProductReceipt')


class ProductReceipt(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_receipts')
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='product_receipts')
    quantity = models.PositiveIntegerField()


class CategoryPlace(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    average_receipt = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
