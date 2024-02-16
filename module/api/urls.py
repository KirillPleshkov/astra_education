from django.urls import path

from module.api.views import GetModuleView

urlpatterns = [
    path('/<int:pk>', GetModuleView.as_view())
]