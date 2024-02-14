from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', include('auth.api.urls')),
    path('users/', include('users.api.urls')),
    path('discipline', include('discipline.api.urls'))
]
