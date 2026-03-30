from django.urls import path
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- FUNÇÃO 1: FORMULÁRIO DE CADASTRO ---
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
            return HttpResponse("<h1>✅ Sucesso!</h1><p>Paciente cadastrado.</p><a href='/'>Cadastrar outro</a> | <a href='/lista'>Ver Lista</a>")
        except Exception as e:
            return HttpResponse(f"<h1>❌ Erro</h1><p>{e}</p>")

    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>Cadastro - Sempre Vida</title>
    </head>
    <body class="bg-light">
        <div class="container mt-5" style="max-width: 500px; background: white; padding: 30px; border-radius: 15px; shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 class="text-center mb-4">🩺 Cadastro de Paciente</h2>
            <form method="POST">
                <div class="mb-3"><label class="form-label">Nome</label><input type="text" name="nome" class="form-control" required></div>
                <div class="mb-3"><label class="form-label">WhatsApp</label><input type="text" name="whatsapp" class="form-control"></div>
                <div class="mb-3"><label class="form-label">Data da Consulta</label><input type="date" name="data" class="form-control"></div>
                <div class="mb-3"><label class="form-label">Observações</label><textarea name="obs" class="form-control"></textarea></div>
                <button type="submit" class="btn btn-primary w-100">Salvar no Banco de Dados</button>
            </form>
            <div class="text-center mt-3"><a href="/lista" class="btn btn-outline-secondary btn-sm">Ver Lista de Pacientes</a></div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

# --- FUNÇÃO 2: LISTA DE PACIENTES ---
def lista_pacientes(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nome, whatsapp, data_consulta FROM pacientes ORDER BY criado_em DESC")
            pacientes = cursor.fetchall()
        
        # Montando as linhas da tabela em HTML
        linhas = ""
        for p in pacientes:
            linhas += f"<tr><td>{p[0]}</td><td>{p[1]}</td><td>{p[2]}</td></tr>"

        html_lista = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Lista de Pacientes - Sempre Vida</title>
        </head>
        <body class="bg-light p-5">
            <div class="container bg-white p-4 rounded shadow">
                <h2 class="mb-4">📋 Lista de Pacientes Cadastrados</h2>
                <table class="table table-striped">
                    <thead class="table-dark">
                        <tr><th>Nome</th><th>WhatsApp</th><th>Data Consulta</th></tr>
                    </thead>
                    <tbody>
                        {linhas}
                    </tbody>
                </table>
                <a href="/" class="btn btn-primary">Voltar ao Cadastro</a>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html_lista)
    except Exception as e:
        return HttpResponse(f"<h1>❌ Erro ao carregar lista</h1><p>{e}</p>")

# --- ROTAS DO SITE ---
urlpatterns = [
    path('', formulario_paciente), # Página inicial
    path('lista/', lista_pacientes), # Nova página: seu-site.com/lista/
]
