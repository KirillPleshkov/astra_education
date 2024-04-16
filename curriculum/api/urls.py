from django.urls import path, include
from rest_framework.routers import DefaultRouter

from curriculum.api.views import CurriculumViewSet, GetEducationalLevelView

router = DefaultRouter()
router.register(r'', CurriculumViewSet, basename='curriculum')

urlpatterns = [
    path('educational_level/', GetEducationalLevelView.as_view()),
    path('', include(router.urls))
]
