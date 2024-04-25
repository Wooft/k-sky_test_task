
from django.urls import path
from analytics.views import AnalyticsView, PlaceView

urlpatterns = [
    path('analytics/', AnalyticsView.as_view({'get': 'list'})),
    path('places/', PlaceView.as_view({'get': 'list'}))
]
