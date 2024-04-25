from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from analytics.models import Receipt, Place, CategoryPlace
from analytics.serializers import ReceiptSerializer, PlaceSerializer, CategoryPlaceSerializer


class AnalyticsView(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def list(self, request, *args, **kwargs):
        """
        Получает и возвращает список мест покупок с дополнительной аналитикой по категориям.

        Этот метод обрабатывает GET-запросы на получение списка объектов. Для каждого объекта
        в списке дополнительно извлекает данные аналитики по категориям мест. Возвращает данные
        в формате JSON.

        Параметры:
            request: HttpRequest - HTTP запрос от клиента.
            *args: Список аргументов переменной длины.
            **kwargs: Словарь ключевых аргументов.

        Возвращает:
            Response: HttpResponse содержащий сериализованные данные мест покупок и аналитику по категориям.
        """
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


