from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
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
            body {{ background-color: #f0f2f5; padding: 15px; font-family: 'Segoe UI', sans-serif; }}
            .card-box {{ max-width: 500px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
            .btn-menu {{ padding: 20px; font-size: 1.2rem; font-weight: bold; border-radius: 15px; margin-bottom: 15px; display: flex; align-items: center; justify-content: center; gap: 15px; text-decoration: none; transition: 0.3s; }}
            .btn-menu:hover {{ transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
            .btn-unidade {{ background-color: #198754; color: white; }}
            .btn-especialidade {{ background-color: #0d6efd; color: white; }}
            .btn-save {{ padding: 12px; font-weight: bold; border-radius: 10px; }}
            .unidade-item {{ border-bottom: 1px solid #eee; padding: 12px 0; }}
        </style>
    </head>
    <body>
        <div class="card-box">
            {conteudo}
        </div>
    </body>
    </html>
    """

# --- TELA 0: PAINEL DE CONTROLE GERAL ---
def painel_controle(request):
    conteudo = """
        <div class="text-center mb-4">
            <h2 class="fw-bold">Painel de Gestão</h2>
            <p class="text-muted">Sistema Sempre Vida</p>
        </div>
        <div class="d-grid">
            <a href="/unidades/" class="btn-menu btn-unidade">
                <span>🏢</span> Unidades
            </a>
            <a href="/especialidades/" class="btn-menu btn-especialidade">
                <span>🏥</span> Especialidades
            </a>
            <button class="btn btn-light btn-menu text-muted" disabled>
                <span>👤</span> Médico/Dentista (Em breve)
            </button>
            <button class="btn btn-light btn-menu text-muted" disabled>
                <span>💰</span> Financeiro (Em breve)
            </button>
        </div>
    """
    return HttpResponse(base_html("Painel Geral", conteudo))

# --- TELA 1: CADASTRO DE UNIDADE ---
@csrf_exempt
def cadastro_unidade(request):
    mensagem = ""
    if request.method == "POST":
        nome, end, tel = request.POST.get('nome'), request.POST.get('endereco'), request.POST.get('telefone')
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO unidades (nome, endereco, telefone) VALUES (%s, %s, %s)", [nome, end, tel])
            mensagem = '<div class="alert alert-success">✅ Unidade Cadastrada!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    conteudo = f"""
        <h3 class="text-center mb-4">🏢 Nova Unidade</h3>
        {mensagem}
        <form method="POST">
            <input type="text" name="nome" class="form-control mb-2" placeholder="Nome" required>
            <input type="text" name="endereco" class="form-control mb-2" placeholder="Endereço">
            <input type="text" name="telefone" class="form-control mb-2" placeholder="Telefone">
            <button type="submit" class="btn btn-success w-100 btn-save">Salvar Unidade</button>
        </form>
        <div class="mt-4 d-grid gap-2 text-center">
            <a href="/unidades/lista/" class="btn btn-outline-primary fw-bold">📋 Listar Unidades</a>
            <a href="/" class="btn btn-link">⬅️ Voltar ao Painel</a>
        </div>
    """
    return HttpResponse(base_html("Cadastro Unidade", conteudo))

# --- TELA: LISTAGEM DE UNIDADES ---
def lista_unidades(request):
    if request.GET.get('delete'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM unidades WHERE id = %s", [request.GET.get('delete')])
        return HttpResponseRedirect('/unidades/lista/')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, endereco FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()

    itens = "".join([f'<div class="unidade-item d-flex justify-content-between"><div><b>{u[1]}</b><br><small>{u[2]}</small></div><a href="/unidades/lista/?delete={u[0]}" class="btn btn-sm btn-outline-danger align-self-center">Excluir</a></div>' for u in unidades])
    
    conteudo = f"""
        <h3 class="text-center mb-4">📋 Unidades Ativas</h3>
        {itens if unidades else '<p class="text-muted">Nenhuma unidade.</p>'}
        <div class="mt-4 d-grid gap-2">
            <a href="/unidades/" class="btn btn-primary btn-save">➕ Nova Unidade</a>
            <a href="/" class="btn btn-outline-secondary">⬅️ Painel Geral</a>
        </div>
    """
    return HttpResponse(base_html("Lista Unidades", conteudo))

# --- TELA 2: ESPECIALIDADES ---
@csrf_exempt
def especialidades_geral(request):
    mensagem = ""
    if request.GET.get('delete_esp'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM especialidades WHERE id = %s", [request.GET.get('delete_esp')])
        return HttpResponseRedirect('/especialidades/')

    if request.method == "POST":
        nome, tipo = request.POST.get('nome'), request.POST.get('tipo')
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO especialidades (nome, tipo) VALUES (%s, %s)", [nome, tipo])
            mensagem = '<div class="alert alert-success">✅ Especialidade Salva!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, tipo FROM especialidades ORDER BY tipo, nome")
        dados = cursor.fetchall()

    itens = "".join([f'<div class="unidade-item d-flex justify-content-between"><div><b>{d[1]}</b><br><small class="badge bg-info">{d[2]}</small></div><a href="/especialidades/?delete_esp={d[0]}" class="btn btn-sm btn-outline-danger align-self-center">Excluir</a></div>' for d in dados])

    conteudo = f"""
        <h3 class="text-center mb-4">🏥 Especialidades</h3>
        {mensagem}
        <form method="POST" class="mb-4">
            <input type="text" name="nome" class="form-control mb-2" placeholder="Ex: Pediatria" required>
            <select name="tipo" class="form-select mb-2">
                <option value="Médica">Médica</option>
                <option value="Odontológica">Odontológica</option>
            </select>
            <button type="submit" class="btn btn-primary w-100 btn-save">Salvar Especialidade</button>
        </form>
        {itens}
        <div class="mt-4 text-center">
            <a href="/" class="btn btn-outline-secondary w-100">⬅️ Voltar ao Painel</a>
        </div>
    """
    return HttpResponse(base_html("Especialidades", conteudo))

# --- ROTAS (PAINEL GERAL NO TOPO) ---
urlpatterns = [
    path('', painel_controle),             # Página Principal agora é o Painel
    path('unidades/', cadastro_unidade),
    path('unidades/lista/', lista_unidades),
    path('especialidades/', especialidades_geral),
]
