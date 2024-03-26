from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', include('auth.api.urls')),
    path('user/', include('user.api.urls')),
    path('discipline/', include('discipline.api.urls')),
    path('module/', include('module.api.urls')),
    path('block/', include('block.api.urls')),
    path('curriculum/', include('curriculum.api.urls'))
]
