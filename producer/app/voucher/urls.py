from django.contrib import admin
from django.urls import path
from voucher.views import ChecksViewSet

urlpatterns = [
    path('admin/', admin.site.urls),\
    path('checks/', ChecksViewSet.as_view({'post': 'create'}), name='checks'),
]