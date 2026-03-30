from django.urls import path
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- ESTILO CSS COMUM (PARA FICAR BONITO NO CELULAR) ---
def get_html_template(titulo, conteudo):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>{titulo}</title>
        <style>
            body {{ background-color: #f8f9fa; font-size: 16px; }}
            .container-main {{ width: 95%; max-width: 500px; margin: 20px auto; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .btn-lg-custom {{ padding: 12px; font-size: 1.1rem; }}
        </style>
    </head>
    <body>
        <div class="container-main">
            {conteudo}
        </div>
    </body>
    </html>
    """

# --- 1. PACIENTES (PÁGINA INICIAL) ---
@csrf_exempt
def formulario_paciente(request):
    mensagem = ""
    if request.method == "POST":
        nome = request.POST.get('nome')
        whatsapp = request.POST.get('whatsapp')
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO pacientes (nome, whatsapp) VALUES (%s, %s)", [nome, whatsapp])
            mensagem = '<div class="alert alert-success">✅ Paciente Salvo!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    conteudo = f"""
        <h2 class="text-center mb-4">🩺 Cadastro Paciente</h2>
        {mensagem}
        <form method="POST">
            <div class="mb-3"><label class="form-label">Nome</label><input type="text" name="nome" class="form-control" required></div>
            <div class="mb-3"><label class="form-label">WhatsApp</label><input type="text" name="whatsapp" class="form-control"></div>
            <button type="submit" class="btn btn-primary w-100 btn-lg-custom">Salvar Paciente</button>
        </form>
        <hr>
        <div class="d-grid gap-2">
            <a href="/unidades/" class="btn btn-outline-success">🏢 Gerenciar Unidades</a>
            <a href="/lista/" class="btn btn-outline-secondary">📋 Lista de Pacientes</a>
        </div>
    """
    return HttpResponse(get_html_template("Sempre Vida - Cadastro", conteudo))

# --- 2. UNIDADES (CADASTRO) ---
@csrf_exempt
def cadastro_unidade(request):
    mensagem = ""
    if request.method == "POST":
        nome = request.POST.get('nome')
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO unidades (nome) VALUES (%s)", [nome])
            mensagem = '<div class="alert alert-success">✅ Unidade Cadastrada com Sucesso!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    conteudo = f"""
        <h2 class="text-center mb-4">🏢 Nova Unidade</h2>
        {mensagem}
        <form method="POST">
            <div class="mb-3"><label class="form-label">Nome da Unidade</label><input type="text" name="nome" class="form-control" required placeholder="Ex: Unidade Centro"></div>
            <button type="submit" class="btn btn-success w-100 btn-lg-custom">Salvar Unidade</button>
        </form>
        <div class="text-center mt-3">
            <a href="/unidades/lista/" class="btn btn-link">Ver Unidades</a> | 
            <a href="/" class="btn btn-link">Voltar ao Início</a>
        </div>
    """
    return HttpResponse(get_html_template("Sempre Vida - Unidades", conteudo))

# --- 3. LISTAGEM DE UNIDADES ---
def lista_unidades(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()
    
    linhas = "".join([f"<tr><td>{u[1]}</td><td><button class='btn btn-sm btn-danger'>Excluir</button></td></tr>" for u in unidades])
    
    conteudo = f"""
        <h3 class="mb-4">📋 Unidades</h3>
        <table class="table">
            <thead><tr><th>Nome</th><th>Ação</th></tr></thead>
            <tbody>{linhas}</tbody>
        </table>
        <a href="/unidades/" class="btn btn-primary w-100">Nova Unidade</a>
        <a href="/" class="btn btn-link w-100 mt-2">Início</a>
    """
    return HttpResponse(get_html_template("Lista de Unidades", conteudo))

# --- ROTAS (URLS) ---
urlpatterns = [
    path('', formulario_paciente),          # Página Inicial (Caminho Vazio)
    path('unidades/', cadastro_unidade),    # Cadastro de Unidades
    path('unidades/lista/', lista_unidades),# Lista de Unidades
]
