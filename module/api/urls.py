from django.urls import path, include

from module.api.views import ModuleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ModuleViewSet, basename='module_get')

urlpatterns = [
    path('', include(router.urls)),
]

