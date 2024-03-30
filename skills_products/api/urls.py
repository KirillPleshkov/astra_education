from django.urls import path, include
from rest_framework.routers import DefaultRouter

from skills_products.api.views import ProductViewSet, SkillViewSet

router = DefaultRouter()

router.register(r'skill', SkillViewSet, basename='skill')
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]