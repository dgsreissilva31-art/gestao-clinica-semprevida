from django.urls import path
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- FUNÇÃO 1: FORMULÁRIO DE CADASTRO (OTIMIZADO MOBILE) ---
@csrf_exempt
def formulario_paciente(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        whatsapp = request.POST.get('whatsapp')
        data_c = request.POST.get('data')
        obs = request.POST.get('obs')

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pacientes (nome, whatsapp, data_consulta, observacoes) VALUES (%s, %s, %s, %s)",
                    [nome, whatsapp, data_c, obs]
                )
            return HttpResponse("<meta name='viewport' content='width=device-width, initial-scale=1'><div style='padding:20px; text-align:center;'><h1>✅ Sucesso!</h1><a href='/' style='display:block; margin-top:20px; font-size:20px;'>Cadastrar outro</a><br><a href='/lista' style='font-size:20px;'>Ver Lista</a></div>")
        except Exception as e:
            return HttpResponse(f"<h1>❌ Erro</h1><p>{e}</p>")

    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>Sempre Vida - Cadastro</title>
        <style>
            body { background-color: #f8f9fa; }
            .card-mobile { width: 95%; max-width: 500px; margin: 20px auto; padding: 25px; border-radius: 15px; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            .btn-lg-custom { padding: 15px; font-size: 1.2rem; }
            input, textarea { font-size: 16px !important; } /* Evita zoom automático no iPhone */
        </style>
    </head>
    <body>
        <div class="card-mobile">
            <h2 class="text-center mb-4">🩺 Cadastro Sempre Vida</h2>
            <form method="POST">
                <div class="mb-3"><label class="form-label fw-bold">Nome Completo</label><input type="text" name="nome" class="form-control form-control-lg" required></div>
                <div class="mb-3"><label class="form-label fw-bold">WhatsApp</label><input type="tel" name="whatsapp" class="form-control form-control-lg" placeholder="(00) 00000-0000"></div>
                <div class="mb-3"><label class="form-label fw-bold">Data da Consulta</label><input type="date" name="data" class="form-control form-control-lg"></div>
                <div class="mb-3"><label class="form-label fw-bold">Observações</label><textarea name="obs" class="form-control" rows="3"></textarea></div>
                <button type="submit" class="btn btn-primary w-100 btn-lg-custom shadow">Salvar Dados</button>
            </form>
            <div class="text-center mt-4"><a href="/lista" class="text-decoration-none text-secondary">📋 Ver lista de cadastrados</a></div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

# --- FUNÇÃO 2: LISTA DE PACIENTES (OTIMIZADA MOBILE) ---
def lista_pacientes(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nome, whatsapp, data_consulta FROM pacientes ORDER BY criado_em DESC")
            pacientes = cursor.fetchall()
        
        linhas = ""
        for p in pacientes:
            linhas += f"<tr><td>{p[0]}</td><td class='text-nowrap'>{p[1]}</td><td>{p[2]}</td></tr>"

        html_lista = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Sempre Vida - Lista</title>
            <style>
                body {{ background-color: #f8f9fa; font-size: 14px; }}
                .container-mobile {{ width: 98%; margin: 10px auto; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
                .table-responsive {{ border: none; }}
                th {{ font-size: 12px; text-transform: uppercase; }}
            </style>
        </head>
        <body>
            <div class="container-mobile">
                <h3 class="mb-3 text-center">📋 Pacientes</h3>
                <div class="table-responsive">
                    <table class="table table-hover table-sm">
                        <thead class="table-primary">
                            <tr><th>Nome</th><th>WhatsApp</th><th>Data</th></tr>
                        </thead>
                        <tbody>
                            {linhas}
                        </tbody>
                    </table>
                </div>
                <div class="mt-4"><a href="/" class="btn btn-outline-primary w-100">Voltar ao Cadastro</a></div>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html_lista)
    except Exception as e:
        return HttpResponse(f"<h1>❌ Erro ao carregar lista</h1><p>{e}</p>")

# --- ROTAS ---
urlpatterns = [
    path('', formulario_paciente),
    path('lista/', lista_pacientes),
]
