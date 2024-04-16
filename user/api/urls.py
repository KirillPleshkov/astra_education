from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.api.views import GetUser, TeacherViewSet

router = DefaultRouter()
router.register(r'', TeacherViewSet, basename='teacher')

urlpatterns = [
    path('', GetUser.as_view()),
    path('teacher/', include(router.urls))
]
