from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import StationViewSet

router = DefaultRouter()
router.register(r'stations', StationViewSet, basename='stations')

urlpatterns = [
    path('v1/', include(router.urls))
]
