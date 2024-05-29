from django.urls import path

from block.api.views import FileDownloadView, FileUploadView

app_name = 'block'

urlpatterns = [
    path('file/<int:pk>', FileDownloadView.as_view(), name='file_download'),
    path('file/upload', FileUploadView.as_view(), name='file_upload')
]
