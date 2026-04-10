from django.shortcuts import render
from .models import Agendamento
from datetime import date

def dashboard_clinica(request):
    hoje = date.today()
    
    # Busca os agendamentos de hoje no banco de dados
    agendados_hoje = Agendamento.objects.filter(data=hoje).count()
    
    # Busca o total geral para o card de desempenho
    total_geral = Agendamento.objects.all().count()

    context = {
        'agendados_hoje': agendados_hoje,
        'total_geral': total_geral,
        'data_atual': hoje.strftime('%d/%m/%Y')
    }








