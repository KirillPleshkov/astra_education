from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from module.api.permitions import IsOwnerStudent
from module.api.serializers import ModuleSerializer
from module.models import Module


class ModuleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerStudent]
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()

    def retrieve(self, request, pk=None):
        module = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, module)

        serializer = self.serializer_class(module)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, instance)

        serializer = self.serializer_class(data=request.data, instance=instance)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
