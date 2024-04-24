from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from skills_products.api.serializers import SkillSerializer, ProductSerializer
from skills_products.models import Skill, Product


# Create your views here.
class SkillViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()

    def list(self, request):
        skill_name = request.query_params.get('name')
        serializer = self.serializer_class(self.queryset.filter(name__icontains=skill_name), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def list(self, request):
        product_name = request.query_params.get('name')
        serializer = self.serializer_class(self.queryset.filter(name__icontains=product_name), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
