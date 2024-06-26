# Generated by Django 5.0.4 on 2024-04-23 21:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productvoucher', to='voucher.product')),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('transaction_id', models.IntegerField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nds_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tips_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_method', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=250)),
                ('items', models.ManyToManyField(through='voucher.ProductVoucher', to='voucher.product')),
            ],
        ),
        migrations.AddField(
            model_name='productvoucher',
            name='voucher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productvoucher', to='voucher.voucher'),
        ),
    ]
