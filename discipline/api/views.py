import os
from datetime import datetime

from django.contrib.staticfiles import finders
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import ProtectedError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template
from django.views import View
from reportlab.lib.colors import HexColor
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from xhtml2pdf.files import pisaFileObject

from astra_education import settings
from block.models import Block
from discipline.api.serializers import DisciplineSerializer, DisciplineNameSerializer
from discipline.models import Discipline
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
import io
from reportlab.lib import colors

from module.models import Module
from xhtml2pdf import pisa


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


def link_callback(uri, rel):
    if isinstance(uri, WSGIRequest):
        path = uri.get_full_path()
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        path = uri
    if not os.path.isfile(path):
        raise Exception(f"Path does not exist: {path}")
    pisaFileObject.getNamedFile = lambda self: path
    print(path)
    return path


class DisciplinePdfView(APIView):
    def get(self, request, pk):
        discipline = Discipline.objects.get(pk=pk)

        blocks = list(Block.objects.filter(module__in=discipline.modules.all()).order_by('position'))
        blocks = [{'files': block.files.order_by('position'), 'module': block.module, 'name': block.name, 'main_text': block.main_text.replace('\n', '</br >')} for
                  block in blocks]

        template_path = 'discipline.html'
        context = {'name': discipline.name, 'short_description': discipline.short_description.replace('\n', '</br >'),
                   'skills': discipline.skills.all(), 'products': discipline.products.all(),
                   'modules': discipline.modules.all().order_by('disciplinemodule__position'),
                   'blocks': blocks}

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{discipline.name}.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)

        if pisa_status.err:
            return HttpResponse('We had some errors')
        return response
