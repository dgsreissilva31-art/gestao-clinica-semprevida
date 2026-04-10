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

def login_view(request):
    mensagem = ""

    if request.method == "POST":
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("senha")
        )

        if user:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            mensagem = "Login inválido"

    return HttpResponse(f"""
        <h3>Login</h3>
        {mensagem}
        <form method="POST">
            <input name="username" placeholder="Usuário"><br>
            <input name="senha" type="password" placeholder="Senha"><br>
            <button>Entrar</button>
        </form>
    """)
    return render(request, 'dashboard.html', context)
