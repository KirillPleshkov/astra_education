from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from module.api.permitions import IsOwnerStudent
from module.api.serializers import ModuleSerializer
from module.models import Module


class GetModuleView(APIView):
    # permission_classes = [IsAuthenticated, IsOwnerStudent]
    serializer_class = ModuleSerializer

    def get(self, request, pk):
        module = Module.objects.get(pk=pk)
        serializer = self.serializer_class(module)

        self.check_object_permissions(self.request,  module)
        return Response(serializer.data)
