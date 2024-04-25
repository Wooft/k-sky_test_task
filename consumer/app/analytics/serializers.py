from rest_framework import serializers

from analytics.models import Receipt, Place, CategoryPlace, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model = Category
        fields = ('name', )

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta():
        model = Receipt
        fields = "__all__"

class PlaceSerializer(serializers.ModelSerializer):
    class Meta():
        model = Place
        fields = "__all__"

class CategoryPlaceSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    class Meta():
        model = CategoryPlace
        fields = ('category', 'total_spent', 'average_receipt')