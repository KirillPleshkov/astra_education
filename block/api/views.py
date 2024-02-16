from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from block.api.serializers import BlockFilesSerializer
from block.models import BlockFiles


# Create your views here.


class GetFileView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = BlockFilesSerializer

    def get(self, request, pk):
        queryset = BlockFiles.objects.get(pk=pk)
        file_handle = queryset.file.path
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/msword')
        response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.file.name
        return response
