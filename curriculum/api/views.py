from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from curriculum.api.serializers import CurriculumSerializer, CurriculumNameSerializer
from curriculum.models import Curriculum


class CurriculumViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated, IsOwnerStudent]
    queryset = Curriculum.objects.all()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'create'):
            return CurriculumSerializer
        return CurriculumNameSerializer

    def retrieve(self, request, pk=None):
        curriculum = get_object_or_404(self.queryset, pk=pk)
        # self.check_object_permissions(self.request, module)

        serializer = self.get_serializer_class()(curriculum)
        return Response(serializer.data)

    def list(self, request):
        curriculum_name = request.query_params.get('name')
        serializer = self.get_serializer_class()(self.queryset.filter(name__icontains=curriculum_name), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
