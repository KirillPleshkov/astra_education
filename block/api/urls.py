from django.urls import path

from block.api.views import FileDownloadView, FileUploadView

urlpatterns = [
    path('file/<int:pk>', FileDownloadView.as_view()),
    path('file/upload', FileUploadView.as_view())
]
