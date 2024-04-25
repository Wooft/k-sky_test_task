from analytics.models import Place, Taxes, Receipt, Category, Product, ProductReceipt, CategoryPlace
from consumer.celery import app
from django.db.models import Sum, Avg, Count
from django.db.models import F
from pprint import pprint

@app.task
def analytics_calculation():
    for place in Place.objects.all():
        taxes = Taxes.objects.get_or_create(place=place)[0]
        data = Receipt.objects.filter(place=place).aggregate(total_nds=Sum('nds_amount'),
                                                             total_tips=Sum('tips_amount'),
                                                             avg_receipt=Avg('total_amount'))
        taxes.total_nds = data['total_nds']
        taxes.total_tips = data['total_tips']
        taxes.save()
        place.average_receipt = data['avg_receipt']
        place.total_purchases = Receipt.objects.filter(place=place).count()
        place.save()

        #получить сумму всех покупок по категориями
        category_totals = ProductReceipt.objects.filter(
            receipt__place_id=place
        ).values(
            'product__category'
        ).annotate(
            total_spent=Sum(F('quantity') * F('product__price'))
        ).order_by('product__category')

        for category_total in category_totals:
            cat = Category.objects.filter(id=category_total['product__category']).first()
            catplace = CategoryPlace.objects.get_or_create(place=place, category=cat)[0]
            catplace.total_spent = category_total['total_spent']
            catplace.save()

        category_averages = Receipt.objects.filter(
            place=place
        ).values(
            'products__category'
        ).annotate(
            average_receipt=Avg('total_amount')
        ).order_by('products__category')

        for category_average in category_averages:
            catplace = CategoryPlace.objects.get_or_create(place=place, category=category_average['products__category'])[0]
            catplace.average_receipt = category_average['average_receipt']
            catplace.save()