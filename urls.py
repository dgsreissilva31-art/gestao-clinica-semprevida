from django.urls import path
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def formulario_paciente(request):
    if request.method == "POST":
        # Pega os dados vindos do formulário
        nome = request.POST.get('nome')
        whatsapp = request.POST.get('whatsapp')
        data_c = request.POST.get('data')
        obs = request.POST.get('obs')

        # Salva no Banco de Dados (Supabase)
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pacientes (nome, whatsapp, data_consulta, observacoes) VALUES (%s, %s, %s, %s)",
                    [nome, whatsapp, data_c, obs]
                )
            return HttpResponse("<h1>✅ Sucesso!</h1><p>Paciente cadastrado no banco de dados da Clínica.</p><a href='/'>Cadastrar outro</a>")
        except Exception as e:
            return HttpResponse(f"<h1>❌ Erro ao salvar</h1><p>{e}</p>")

    # O formulário visual (HTML)
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>Cadastro - Clínica Sempre Vida</title>
    </head>
    <body class="bg-light">
        <div class="container mt-5" style="max-width: 500px; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 class="text-center mb-4">🩺 Cadastro de Paciente</h2>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label font-weight-bold">Nome Completo</label>
                    <input type="text" name="nome" class="form-control" placeholder="Ex: João Silva" required>
                </div>
                <div class="mb-3">
                    <label class="form-label font-weight-bold">WhatsApp</label>
                    <input type="text" name="whatsapp" class="form-control" placeholder="(00) 00000-0000">
                </div>
                <div class="mb-3">
                    <label class="form-label font-weight-bold">Data da Consulta</label>
                    <input type="date" name="data" class="form-control">
                </div>
                <div class="mb-3">
                    <label class="form-label font-weight-bold">Observações</label>
                    <textarea name="obs" class="form-control" rows="3"></textarea>
                </div>
                <button type="submit" class="btn btn-primary w-100 py-2">Salvar no Banco de Dados</button>
            </form>
            <hr>
            <p class="text-center text-muted small">Consultoria IA.naEmpresa</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', formulario_paciente),
]
