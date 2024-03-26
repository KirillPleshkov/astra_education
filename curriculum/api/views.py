from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from curriculum.api.serializers import CurriculumSerializer
from curriculum.models import Curriculum


class CurriculumViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated, IsOwnerStudent]
    serializer_class = CurriculumSerializer
    queryset = Curriculum.objects.all()

    def retrieve(self, request, pk=None):
        curriculum = get_object_or_404(self.queryset, pk=pk)
        # self.check_object_permissions(self.request, module)

        serializer = self.serializer_class(curriculum)
        return Response(serializer.data)
