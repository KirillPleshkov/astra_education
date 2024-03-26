from django.urls import path, include
from rest_framework.routers import DefaultRouter

from discipline.api.views import DisciplineViewSet

router = DefaultRouter()
router.register(r'', DisciplineViewSet, basename='discipline')

urlpatterns = [
    path('', include(router.urls)),
]
