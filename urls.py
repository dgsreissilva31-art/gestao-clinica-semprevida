from django.urls import path
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- TEMPLATE BASE (DESIGN SEMPRE VIDA) ---
def base_html(titulo, conteudo):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>{titulo} - Sempre Vida</title>
        <style>
            body {{ background-color: #f0f2f5; padding: 15px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
            .card-box {{ max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
            .btn-save {{ padding: 15px; font-size: 1.1rem; font-weight: bold; border-radius: 10px; transition: 0.3s; }}
            .btn-save:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
            .form-label {{ font-weight: 600; color: #495057; }}
            .form-control-lg {{ border-radius: 10px; font-size: 1rem; }}
        </style>
    </head>
    <body>
        <div class="card-box">
            {conteudo}
        </div>
    </body>
    </html>
    """

# --- TELA 1: CADASTRO DE NOVA UNIDADE ---
@csrf_exempt
def cadastro_unidade(request):
    mensagem = ""
    if request.method == "POST":
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        telefone = request.POST.get('telefone')
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO unidades (nome, endereco, telefone) VALUES (%s, %s, %s)", 
                    [nome, endereco, telefone]
                )
            mensagem = '<div class="alert alert-success shadow-sm">✅ Unidade Cadastrada com Sucesso!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    conteudo = f"""
        <div class="text-center mb-4">
            <span style="font-size: 50px;">🏢</span>
            <h2 class="mt-2">Nova Unidade</h2>
            <p class="text-muted">Cadastre as unidades da rede Sempre Vida</p>
        </div>
        {mensagem}
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">Nome da Unidade</label>
                <input type="text" name="nome" class="form-control form-control-lg" placeholder="Ex: Unidade Centro" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Endereço Completo</label>
                <input type="text" name="endereco" class="form-control form-control-lg" placeholder="Rua, Número, Bairro">
            </div>
            <div class="mb-3">
                <label class="form-label">Telefone de Contato</label>
                <input type="tel" name="telefone" class="form-control form-control-lg" placeholder="(00) 0000-0000">
            </div>
            <button type="submit" class="btn btn-success w-100 btn-save mt-3">Salvar Unidade</button>
        </form>
        <div class="text-center mt-4">
            <a href="/unidades/lista/" class="btn btn-outline-primary w-100 border-0">📋 Ir para Listagem de Unidades</a>
        </div>
    """
    return HttpResponse(base_html("Nova Unidade", conteudo))

# --- TELA 2: LISTAGEM DE UNIDADES (COM EDITAR/EXCLUIR) ---
def lista_unidades(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome, endereco, telefone FROM unidades ORDER BY nome ASC")
            unidades = cursor.fetchall()
        
        linhas = ""
        for u in unidades:
            linhas += f"""
            <div class="border-bottom py-3">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <strong style="font-size: 1.1rem; color: #2c3e50;">{u[1]}</strong><br>
                        <small class="text-muted">📍 {u[2] if u[2] else 'Sem endereço'}</small><br>
                        <small class="text-muted">📞 {u[3] if u[3] else 'Sem telefone'}</small>
                    </div>
                    <div class="d-flex gap-1">
                        <button class="btn btn-sm btn-outline-warning">Edit</button>
                        <button class="btn btn-sm btn-outline-danger">Sair</button>
                    </div>
                </div>
            </div>"""

        if not unidades:
            linhas = "<p class='text-center text-muted'>Nenhuma unidade cadastrada.</p>"

        conteudo = f"""
            <h3 class="mb-4 text-center">📋 Unidades Ativas</h3>
            <div style="max-height: 400px; overflow-y: auto;">
                {linhas}
            </div>
            <div class="mt-4">
                <a href="/" class="btn btn-primary w-100 btn-save">➕ Nova Unidade</a>
            </div>
        """
        return HttpResponse(base_html("Lista de Unidades", conteudo))
    except Exception as e:
        return HttpResponse(f"Erro no banco: {e}")

# --- ROTAS DO SISTEMA ---
urlpatterns = [
    path('', cadastro_unidade),            # Tela 1: Cadastro (Página Inicial)
    path('unidades/lista/', lista_unidades), # Tela 2: Listagem
]
