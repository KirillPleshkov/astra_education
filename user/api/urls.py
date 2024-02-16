from django.urls import path

from user.api.views import GetUser

urlpatterns = [
    path('', GetUser.as_view())
]
