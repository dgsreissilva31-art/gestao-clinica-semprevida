from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

# Função rápida para testar se o site está vivo
def home(request):
    return HttpResponse("<h1>Clínica Sempre Vida</h1><p>O sistema está online e funcionando!</p>")

urlpatterns = [
    path('admin/', admin.site.core.admin.site.urls if hasattr(admin.site, 'core') else admin.site.urls),
    path('', home), # Isso define a página inicial
]
