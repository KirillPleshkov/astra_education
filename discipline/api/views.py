from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from discipline.api.serializers import DisciplineSerializer
from discipline.models import Discipline


# Create your views here.

class GetDisciplineView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DisciplineSerializer

    def get(self, request, pk):
        discipline = Discipline.objects.get(pk=pk)
        serializer = self.serializer_class(discipline)
        return Response(serializer.data)
