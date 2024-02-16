from django.urls import path

from block.api.views import GetFileView

urlpatterns = [
    path('/file/<int:pk>', GetFileView.as_view())
]