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








from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect

@csrf_exempt
def login_view(request):
    mensagem = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        senha = request.POST.get("senha", "").strip()

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
            return HttpResponseRedirect("/admin-painel/")
        else:
            mensagem = '<div class="alert alert-danger">Login inválido</div>'

    return HttpResponse(f"""
        <h3>Login</h3>
        {mensagem}
        <form method="POST">
            <input name="username" placeholder="Usuário"><br><br>
            <input name="senha" type="password" placeholder="Senha"><br><br>
            <button>Entrar</button>
        </form>
    """)



