from django.urls import path, include
from rest_framework.routers import DefaultRouter

from discipline.api.views import DisciplineViewSet, DisciplinePdfView

router = DefaultRouter()
router.register(r'', DisciplineViewSet, basename='discipline')

urlpatterns = [
    path('', include(router.urls)),
    path('pdf_download/<pk>/', DisciplinePdfView.as_view())
]


