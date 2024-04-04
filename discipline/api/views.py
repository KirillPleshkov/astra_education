from django.db.models import ProtectedError
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from discipline.api.serializers import DisciplineSerializer, DisciplineNameSerializer
from discipline.models import Discipline


# Create your views here.

class DisciplineViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DisciplineSerializer
    queryset = Discipline.objects.all()

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            return DisciplineSerializer
        return DisciplineNameSerializer

    def retrieve(self, request, pk):
        discipline = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer_class()(discipline)
        return Response(serializer.data)

    def list(self, request):
        discipline_name = request.query_params.get('name')
        serializer = self.get_serializer_class()(self.queryset.filter(name__icontains=discipline_name), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk):
        discipline = get_object_or_404(self.queryset, pk=pk)
        try:
            discipline.delete()
            return Response(True)
        except ProtectedError:
            curriculums = [i.name for i in discipline.curriculums.all()]
            return Response({'detail': {'linked_curriculums': curriculums}}, status=404)

    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        # self.check_object_permissions(self.request, instance)

        serializer = self.serializer_class(data=request.data, instance=instance)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

