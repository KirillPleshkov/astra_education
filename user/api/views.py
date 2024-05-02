from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from curriculum.models import CurriculumDiscipline, CurriculumDisciplineUser
from user.api.serializers import UserSerializer, TeacherSerializer

user_model = get_user_model()


class GetUser(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class TeacherViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer
    queryset = user_model.objects.filter(role=user_model.Roles.TEACHER)

    def list(self, request):
        name = request.query_params.get('name')

        if name is not None:
            serializer = self.serializer_class(self.queryset.filter(
                Q(first_name__icontains=name) |
                Q(last_name__icontains=name)
            ), many=True)
            return Response(serializer.data)

        curriculum = request.query_params.get('curriculum')
        discipline = request.query_params.get('discipline')

        curriculum_discipline = CurriculumDiscipline.objects.get(curriculum_id=curriculum, discipline_id=discipline)

        curriculum_discipline_users = CurriculumDisciplineUser.objects.filter(curriculum_discipline=curriculum_discipline)
        teachers = [curriculum_discipline_user.user for curriculum_discipline_user in curriculum_discipline_users]
        serializer = self.serializer_class(teachers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        teacher = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(teacher)
        return Response(serializer.data)
