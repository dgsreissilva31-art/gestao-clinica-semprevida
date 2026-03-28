from django.urls import path
from . import views

urlpatterns = [
    # Quando o usuário acessar a página inicial, ele verá o dashboard
    path('', views.dashboard_clinica, name='dashboard'),
]
