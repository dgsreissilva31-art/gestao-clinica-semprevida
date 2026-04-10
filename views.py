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






# --- LOGIN E LOGOUT DO SISTEMA ---
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect


@csrf_exempt
def login_view(request):
    mensagem = ""

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        senha = request.POST.get("senha", "").strip()

        if not username or not senha:
            mensagem = '<div class="alert alert-warning">Preencha usuário e senha</div>'
        else:
            user = authenticate(username=username, password=senha)

            if user:
                login(request, user)
                return HttpResponseRedirect("/admin-painel/")
            else:
                mensagem = '<div class="alert alert-danger">Login inválido</div>'

    return HttpResponse(f"""
    <html>
    <head>
        <title>Login - Sistema</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">

        <div class="container d-flex justify-content-center align-items-center" style="height:100vh;">
            <div class="card shadow p-4" style="width:350px;">
                
                <h4 class="text-center mb-3">🔐 Acesso ao Sistema</h4>

                {mensagem}

                <form method="POST">
                    <div class="mb-3">
                        <label class="form-label">Usuário</label>
                        <input name="username" class="form-control" placeholder="Digite seu usuário">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Senha</label>
                        <input name="senha" type="password" class="form-control" placeholder="Digite sua senha">
                    </div>

                    <button class="btn btn-primary w-100">Entrar</button>
                </form>

            </div>
        </div>

    </body>
    </html>
    """)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login/")


from django.contrib.auth.decorators import login_required

@login_required
def pacientes_geral(request):
    ...


