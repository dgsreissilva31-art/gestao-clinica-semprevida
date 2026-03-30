from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- NOVO TEMPLATE BASE (ESTILO DASHBOARD PROFISSIONAL) ---
def base_html(titulo, conteudo):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <title>{titulo} - Sempre Vida</title>
        <style>
            :root {{ --sidebar-width: 250px; --top-bg: #3c8dbc; --sidebar-bg: #222d32; }}
            body {{ background-color: #ecf0f5; font-family: 'Source Sans Pro', sans-serif; margin: 0; }}
            
            /* TOPO */
            .navbar-top {{ background-color: var(--top-bg); height: 50px; position: fixed; width: 100%; top: 0; z-index: 1000; color: white; display: flex; align-items: center; padding: 0 15px; border-bottom: 1px solid rgba(0,0,0,0.1); }}
            
            /* SIDEBAR */
            .sidebar {{ background-color: var(--sidebar-bg); width: var(--sidebar-width); height: 100vh; position: fixed; top: 0; left: 0; padding-top: 50px; z-index: 999; transition: 0.3s; }}
            .sidebar-header {{ padding: 15px; color: white; background: #1a2226; font-size: 14px; display: flex; align-items: center; gap: 10px; }}
            .sidebar-menu {{ list-style: none; padding: 0; margin: 0; }}
            .sidebar-menu li a {{ padding: 12px 15px; display: block; color: #b8c7ce; text-decoration: none; border-left: 3px solid transparent; transition: 0.2s; }}
            .sidebar-menu li a:hover {{ background: #1e282c; color: white; border-left-color: #3c8dbc; }}
            .sidebar-menu li a i {{ margin-right: 10px; }}
            .menu-label {{ padding: 10px 15px; font-size: 12px; color: #4b646f; background: #1a2226; text-transform: uppercase; }}

            /* CONTEÚDO PRINCIPAL */
            .main-content {{ margin-left: var(--sidebar-width); padding: 70px 20px 20px; transition: 0.3s; }}
            .card-panel {{ background: white; border-top: 3px solid #d2d6de; border-radius: 3px; box-shadow: 0 1px 1px rgba(0,0,0,0.1); padding: 20px; }}
            
            @media (max-width: 768px) {{
                .sidebar {{ left: -250px; }}
                .main-content {{ margin-left: 0; }}
                .sidebar.active {{ left: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="navbar-top d-flex justify-content-between">
            <div><i class="bi bi-list fs-4" style="cursor:pointer" onclick="document.querySelector('.sidebar').classList.toggle('active')"></i> <span class="ms-2 fw-bold">milestone</span></div>
            <div><i class="bi bi-person-circle"></i> Douglas Silva</div>
        </div>

        <div class="sidebar">
            <div class="sidebar-header">
                <i class="bi bi-person-circle fs-3"></i>
                <div><b>Douglas Silva</b><br><small><i class="bi bi-circle-fill text-success" style="font-size: 8px;"></i> Online</small></div>
            </div>
            <div class="menu-label">Navegação Principal</div>
            <ul class="sidebar-menu">
                <li><a href="/"><i class="bi bi-speedometer2"></i> Painel de Controle</a></li>
                <div class="menu-label">Cadastros</div>
                <li><a href="/unidades/"><i class="bi bi-building"></i> Unidades</a></li>
                <li><a href="/especialidades/"><i class="bi bi-hospital"></i> Especialidades</a></li>
                <li><a href="#"><i class="bi bi-person-badge"></i> Médicos / Dentistas</a></li>
                <div class="menu-label">Operacional</div>
                <li><a href="#"><i class="bi bi-calendar-event"></i> Agendar Consultas</a></li>
                <li><a href="#"><i class="bi bi-cash-stack"></i> Financeiro</a></li>
            </ul>
        </div>

        <div class="main-content">
            <div class="card-panel">
                {conteudo}
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

# --- TELA 0: PAINEL DE CONTROLE GERAL ---
def painel_controle(request):
    conteudo = """
        <div class="mb-4">
            <h3 class="fw-bold"><i class="bi bi-speedometer2"></i> Painel de Gestão</h3>
            <p class="text-muted">Bem-vindo ao sistema de controle Sempre Vida.</p>
        </div>
        <div class="row g-3">
            <div class="col-md-6 col-lg-3">
                <div class="p-3 bg-primary text-white rounded shadow-sm text-center">
                    <i class="bi bi-building fs-1"></i><br><b>Unidades</b><br>
                    <a href="/unidades/" class="btn btn-sm btn-light mt-2">Acessar</a>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="p-3 bg-success text-white rounded shadow-sm text-center">
                    <i class="bi bi-hospital fs-1"></i><br><b>Especialidades</b><br>
                    <a href="/especialidades/" class="btn btn-sm btn-light mt-2">Acessar</a>
                </div>
            </div>
        </div>
    """
    return HttpResponse(base_html("Dashboard", conteudo))

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
        <h4><i class="bi bi-building"></i> Cadastro de Unidade</h4>
        <hr>
        {mensagem}
        <form method="POST" class="row g-3">
            <div class="col-md-6">
                <label class="form-label">Nome da Unidade</label>
                <input type="text" name="nome" class="form-control" required>
            </div>
            <div class="col-md-6">
                <label class="form-label">Telefone</label>
                <input type="text" name="telefone" class="form-control">
            </div>
            <div class="col-12">
                <label class="form-label">Endereço Completo</label>
                <input type="text" name="endereco" class="form-control">
            </div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">Salvar Unidade</button>
                <a href="/unidades/lista/" class="btn btn-outline-secondary">Ver Lista</a>
            </div>
        </form>
    """
    return HttpResponse(base_html("Cadastro Unidade", conteudo))

# --- TELA: LISTAGEM DE UNIDADES ---
def lista_unidades(request):
    if request.GET.get('delete'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM unidades WHERE id = %s", [request.GET.get('delete')])
        return HttpResponseRedirect('/unidades/lista/')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, endereco, telefone FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()

    linhas = "".join([f'<tr><td>{u[1]}</td><td>{u[2]}</td><td>{u[3]}</td><td><a href="/unidades/lista/?delete={u[0]}" class="btn btn-sm btn-danger">Excluir</a></td></tr>' for u in unidades])
    
    conteudo = f"""
        <h4><i class="bi bi-list-task"></i> Unidades Ativas</h4>
        <hr>
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark"><tr><th>Nome</th><th>Endereço</th><th>Telefone</th><th>Ação</th></tr></thead>
                <tbody>{linhas if unidades else '<tr><td colspan="4" class="text-center">Nenhuma unidade.</td></tr>'}</tbody>
            </table>
        </div>
        <a href="/unidades/" class="btn btn-primary mt-3">Nova Unidade</a>
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

    itens = "".join([f'<tr><td>{d[1]}</td><td><span class="badge bg-info">{d[2]}</span></td><td><a href="/especialidades/?delete_esp={d[0]}" class="btn btn-sm btn-danger">Deletar</a></td></tr>' for d in dados])

    conteudo = f"""
        <h4><i class="bi bi-hospital"></i> Gerenciar Especialidades</h4>
        <hr>
        {mensagem}
        <form method="POST" class="row g-3 mb-4">
            <div class="col-md-6">
                <label class="form-label">Nome da Especialidade</label>
                <input type="text" name="nome" class="form-control" required>
            </div>
            <div class="col-md-4">
                <label class="form-label">Tipo</label>
                <select name="tipo" class="form-select">
                    <option value="Médica">Médica</option>
                    <option value="Odontológica">Odontológica</option>
                </select>
            </div>
            <div class="col-md-2 d-flex align-items-end">
                <button type="submit" class="btn btn-primary w-100">Salvar</button>
            </div>
        </form>
        <table class="table table-hover">
            <thead><tr><th>Especialidade</th><th>Tipo</th><th>Ação</th></tr></thead>
            <tbody>{itens if dados else '<tr><td colspan="3">Vazio</td></tr>'}</tbody>
        </table>
    """
    return HttpResponse(base_html("Especialidades", conteudo))

# --- ROTAS ---
urlpatterns = [
    path('', painel_controle),
    path('unidades/', cadastro_unidade),
    path('unidades/lista/', lista_unidades),
    path('especialidades/', especialidades_geral),
]
