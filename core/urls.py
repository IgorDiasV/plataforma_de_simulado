from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('questoes.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('simulados/', include('simulados.urls'))
]
