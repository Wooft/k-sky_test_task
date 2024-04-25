from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from analytics.models import Receipt, Place, CategoryPlace
from analytics.serializers import ReceiptSerializer, PlaceSerializer, CategoryPlaceSerializer


class AnalyticsView(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        for element in serializer.data:
            cat_anal = []
            for category in CategoryPlace.objects.filter(place=element['id']):
                cat_serializer = CategoryPlaceSerializer(category)
                cat_anal.append(cat_serializer.data)
            element['category_analytics'] = cat_anal
        return Response(serializer.data)


class PlaceView(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


