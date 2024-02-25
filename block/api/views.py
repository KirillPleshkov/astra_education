from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from block.api.serializers import BlockFilesSerializer
from block.models import BlockFiles


# Create your views here.


class FileDownloadView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = BlockFilesSerializer
    parser_classes = [FileUploadParser]

    def get(self, request, pk):
        queryset = BlockFiles.objects.get(pk=pk)
        file_handle = queryset.file.path
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/msword')
        response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.file.name
        return response


class FileUploadView(APIView):
    permission_classes = []
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = BlockFilesSerializer(data=request.data)
        if file_serializer.is_valid():
            print(file_serializer)
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
