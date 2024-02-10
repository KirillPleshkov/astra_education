from django.urls import path

from users.api.views import GetUser

urlpatterns = [
    path('', GetUser.as_view())
]