from django.urls import path

from discipline.api.views import GetDisciplineView

urlpatterns = [
    path('<int:pk>', GetDisciplineView.as_view())
]
