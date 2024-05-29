from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from xhtml2pdf import pisa

from curriculum.api.serializers import CurriculumSerializer, CurriculumNameSerializer, EducationalLevelSerializer, \
    TeacherCurriculumDisciplinesSerializer
from curriculum.models import Curriculum, EducationalLevel, CurriculumDisciplineUser, CurriculumDiscipline
from discipline.api.views import link_callback
from skills_products.models import Skill, Product
from user.api.serializers import TeacherSerializer

user_model = get_user_model()


class CurriculumViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Curriculum.objects.all()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'create', 'update'):
            return CurriculumSerializer
        return CurriculumNameSerializer

    def retrieve(self, request, pk=None):
        curriculum = get_object_or_404(self.queryset, pk=pk)
        # self.check_object_permissions(self.request, module)

        serializer = self.get_serializer_class()(curriculum)
        return Response(serializer.data)

    def list(self, request):
        curriculum_name = request.query_params.get('name')
        if curriculum_name is not None:
            serializer = self.get_serializer_class()(self.queryset.filter(name__icontains=curriculum_name), many=True)
            return Response(serializer.data)

        if request.query_params.get('teacher'):
            curriculum_discipline_users = CurriculumDisciplineUser.objects.filter(user_id=request.user.id)
            curriculum_disciplines = [curriculum_discipline_users.curriculum_discipline for curriculum_discipline_users
                                      in curriculum_discipline_users]

            serializer = TeacherCurriculumDisciplinesSerializer(curriculum_disciplines, many=True)
            return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk):
        curriculum = get_object_or_404(self.queryset, pk=pk)
        try:
            curriculum.delete()
            return Response(True)
        except ProtectedError:
            curriculum_discipline_user = CurriculumDisciplineUser.objects.filter(
                curriculum_discipline__discipline__in=curriculum.disciplines.all())
            users = [i.user for i in curriculum_discipline_user]
            serializer = TeacherSerializer(users, many=True)
            return Response({'detail': {'linked_students': serializer.data}}, status=404)

    def update(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        # self.check_object_permissions(self.request, instance)

        serializer = self.get_serializer_class()(data=request.data, instance=instance)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class GetEducationalLevelView(APIView):
    serializer_class = EducationalLevelSerializer

    def get(self, request):
        serializer = self.serializer_class(EducationalLevel.objects.all(), many=True)
        return Response(serializer.data)


class CurriculumPdfView(APIView):
    def get(self, request, pk):
        curriculum = Curriculum.objects.get(pk=pk)

        skills = set(Skill.objects.filter(disciplines__curriculums=curriculum))
        products = set(Product.objects.filter(disciplines__curriculums=curriculum))

        disciplines = CurriculumDiscipline.objects.filter(curriculum=curriculum)

        filled_semesters = [semester for semester in range(1, curriculum.educational_level.study_period * 2 + 1) if
                            disciplines.filter(semester=semester)]

        template_path = 'curriculum.html'
        context = {'curriculum': curriculum, 'skills': skills, 'products': products,
                   'semesters': filled_semesters, 'disciplines': disciplines}

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{curriculum.name}.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)

        if pisa_status.err:
            return HttpResponse('We had some errors')
        return response
