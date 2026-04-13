import datetime, urllib.parse, re
from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# --- FUNÇÃO BASE (TOPO CORRETO) ---

def base_html(titulo, conteudo):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <title>{titulo} - Grupo Sempre Vida</title>
        <style>
            :root {{ --sidebar-width: 260px; --top-bg: #3c8dbc; --sidebar-bg: #222d32; }}
            body {{ background-color: #ecf0f5; font-family: 'Segoe UI', sans-serif; margin: 0; overflow-x: hidden; }}
            .navbar-top {{ background-color: var(--top-bg); height: 50px; position: fixed; width: 100%; top: 0; z-index: 1000; color: white; display: flex; align-items: center; padding: 0 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .sidebar {{ background-color: var(--sidebar-bg); width: var(--sidebar-width); height: 100vh; position: fixed; top: 0; left: 0; padding-top: 50px; z-index: 999; overflow-y: auto; transition: all 0.3s; }}
            .main-content {{ margin-left: var(--sidebar-width); padding: 70px 20px 20px; min-height: 100vh; }}
            .card-panel {{ background: white; border-top: 3px solid #3c8dbc; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 20px; }}
        </style>
    </head>
    <body>
        <div class="navbar-top d-flex justify-content-between">
            <div><span class="ms-2 fw-bold text-uppercase">SEMPRE VIDA</span></div>
            <div class="small"><i class="bi bi-person-circle"></i> Douglas Silva | <a href="/logout/" class="text-white text-decoration-none">Sair</a></div>
        </div>
        <div class="sidebar">
            <div style="padding: 20px 15px; color: #4b646f; font-size: 12px; background: #1a2226;">MENU PRINCIPAL</div>
            <ul class="list-unstyled">
                <li><a href="/admin-painel/" style="color: #b8c7ce; padding: 10px 15px; display: block; text-decoration: none;"><i class="bi bi-speedometer2"></i> Dashboard</a></li>
                <li><a href="/recepcao/" style="color: #b8c7ce; padding: 10px 15px; display: block; text-decoration: none;"><i class="bi bi-person-check"></i> Recepção</a></li>
                <li><a href="/unidades/lista/" style="color: #b8c7ce; padding: 10px 15px; display: block; text-decoration: none;"><i class="bi bi-building"></i> Unidades</a></li>
            </ul>
        </div>
        <div class="main-content">
            <div class="card-panel">{conteudo}</div>
        </div>
    </body>
    </html>
    """

# --- 🔒 DECORATOR DE PERMISSÃO (VERSÃO BLINDADA) ---

def cargo_required(cargo_necessario):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseRedirect('/login/')
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT cargo FROM perfis_usuario WHERE user_id = %s", [request.user.id])
                resultado = cursor.fetchone()
            
            if not resultado:
                return HttpResponse("❌ Erro: Usuário sem perfil cadastrado.", status=403)
            
            # Normalização rigorosa: remove espaços, remove acentos (opcional) e coloca em minúsculo
            cargo_usuario = str(resultado[0]).strip().lower()
            cargo_alvo = str(cargo_necessario).strip().lower()

            if cargo_usuario != cargo_alvo:
                conteudo_erro = f"""
                <div class='text-center py-5'>
                    <h1 class='display-1 text-danger'><i class='bi bi-shield-lock'></i></h1>
                    <h2 class='fw-bold'>Acesso Negado</h2>
                    <p class='text-muted'>Sua conta ({resultado[0]}) não tem permissão para acessar o módulo de <b>{cargo_necessario}</b>.</p>
                    <hr class='w-25 mx-auto'>
                    <a href='/admin-painel/' class='btn btn-primary'>Voltar ao Início</a>
                </div>
                """
                return HttpResponse(base_html("Acesso Negado", conteudo_erro), status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# --- 2. LOGIN / LOGOUT ---

@csrf_exempt
def login_view(request):
    mensagem = ""
    if request.method == "POST":
        u = request.POST.get("username", "").strip()
        s = request.POST.get("senha", "").strip()
        user = authenticate(username=u, password=s)
        if user:
            login(request, user)
            return HttpResponseRedirect("/admin-painel/")
        mensagem = '<div class="alert alert-danger">Login ou senha inválidos</div>'
    
    return HttpResponse(f"""
    <html><head><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"></head>
    <body class="bg-light d-flex justify-content-center align-items-center" style="height:100vh;">
        <div class="card shadow p-4" style="width:350px;">
            <h4 class="text-center mb-3">🔐 Sempre Vida</h4>
            {mensagem}
            <form method="POST">
                <div class="mb-3"><label>Usuário</label><input name="username" class="form-control" required></div>
                <div class="mb-3"><label>Senha</label><input name="senha" type="password" class="form-control" required></div>
                <button class="btn btn-primary w-100">Entrar</button>
            </form>
        </div>
    </body></html>
    """)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login/")

# --- 3. VIEWS PROTEGIDAS ---

@login_required
def painel_controle(request):
    conteudo = """
    <h4>Painel de Gestão</h4>
    <p class="text-muted">Bem-vindo ao sistema Sempre Vida.</p>
    <div class="row g-3">
        <div class="col-md-4"><div class="p-3 bg-primary text-white rounded shadow-sm text-center"><i class="bi bi-person-check fs-2"></i><br>Recepção<br><a href="/recepcao/" class="btn btn-sm btn-light mt-2">Abrir</a></div></div>
        <div class="col-md-4"><div class="p-3 bg-dark text-white rounded shadow-sm text-center"><i class="bi bi-building fs-2"></i><br>Unidades<br><a href="/unidades/lista/" class="btn btn-sm btn-light mt-2">Gerenciar</a></div></div>
    </div>
    """
    return HttpResponse(base_html("Dashboard", conteudo))

# --- BLOQUEIO TOTAL EM UNIDADES (CADASTRO E LISTA) ---

@login_required
@cargo_required('Administrador')
def cadastro_unidade(request):
    edit_id = request.GET.get('edit')
    unidade_data = [None, "", "", ""]
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome, endereco, telefone FROM unidades WHERE id = %s", [edit_id])
            unidade_data = cursor.fetchone() or unidade_data
    
    if request.method == "POST":
        id_post = request.POST.get('id_unidade')
        nome, end, tel = request.POST.get('nome'), request.POST.get('endereco'), request.POST.get('telefone')
        with connection.cursor() as cursor:
            if id_post:
                cursor.execute("UPDATE unidades SET nome=%s, endereco=%s, telefone=%s WHERE id=%s", [nome, end, tel, id_post])
            else:
                cursor.execute("INSERT INTO unidades (nome, endereco, telefone) VALUES (%s, %s, %s)", [nome, end, tel])
        return HttpResponseRedirect('/unidades/lista/')
    
    conteudo = f"""
    <h4>Gerenciar Unidade</h4>
    <form method='POST' class='row g-3'>
        <input type='hidden' name='id_unidade' value='{unidade_data[0] or ''}'>
        <div class='col-md-6'><label>Nome</label><input type='text' name='nome' class='form-control' value='{unidade_data[1]}' required></div>
        <div class='col-md-6'><label>Telefone</label><input type='text' name='telefone' class='form-control' value='{unidade_data[3]}'></div>
        <div class='col-12'><label>Endereço</label><input type='text' name='endereco' class='form-control' value='{unidade_data[2]}'></div>
        <div class='col-12'><button type='submit' class='btn btn-primary'>Salvar</button></div>
    </form>
    """
    return HttpResponse(base_html("Unidades", conteudo))

@login_required
@cargo_required('Administrador') # ✅ ADICIONADO PARA BLOQUEAR LISTA TAMBÉM
def lista_unidades(request):
    if request.GET.get('delete'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM unidades WHERE id = %s", [request.GET.get('delete')])
        return HttpResponseRedirect('/unidades/lista/')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, endereco, telefone FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()
    
    linhas = "".join([f"<tr><td>{u[1]}</td><td>{u[2]}</td><td><a href='/unidades/?edit={u[0]}' class='btn btn-sm btn-info text-white'>Editar</a></td></tr>" for u in unidades])
    
    conteudo = f"""
    <div class="d-flex justify-content-between mb-3"><h4>Lista de Unidades</h4><a href="/unidades/" class="btn btn-primary">Nova Unidade</a></div>
    <table class="table table-hover"><thead><tr><th>Nome</th><th>Endereço</th><th>Ação</th></tr></thead><tbody>{linhas}</tbody></table>
    """
    return HttpResponse(base_html("Lista", conteudo))

# --- DEMAIS VIEWS (MANTIDAS INALTERADAS) ---

@login_required
@csrf_exempt
def recepcao_geral(request):
    data_hoje = datetime.date.today()
    with connection.cursor() as cursor:
        cursor.execute("SELECT ag.id, pac.nome, prof.nome, ag.horario_selecionado FROM agendamentos ag JOIN pacientes pac ON ag.paciente_id = pac.id JOIN agendas_config ac ON ag.agenda_config_id = ac.id JOIN profissionais prof ON ac.profissional_id = prof.id WHERE ag.data_agendamento = %s", [data_hoje])
        agenda = cursor.fetchall()
    linhas = "".join([f"<tr><td>{a[3]}</td><td>{a[1]}</td><td>{a[2]}</td></tr>" for a in agenda])
    return HttpResponse(base_html("Recepção", f"<h4>Fila de Espera</h4><table class='table'>{linhas}</table>"))

@login_required
@csrf_exempt
def acesso_geral(request):
    User = get_user_model()
    if request.method == "POST":
        nome, user, senha, cargo = request.POST.get('nome'), request.POST.get('username'), request.POST.get('senha'), request.POST.get('cargo')
        if not User.objects.filter(username=user).exists():
            u_obj = User.objects.create_user(username=user, password=senha)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO perfis_usuario (user_id, nome_completo, cargo) VALUES (%s,%s,%s)", [u_obj.id, nome, cargo])
        return HttpResponseRedirect('/acessos/')
    return HttpResponse(base_html("Acessos", "<h4>Cadastro de Usuários</h4><form method='POST'><input name='username' placeholder='Login' class='form-control mb-2'><input name='senha' type='password' placeholder='Senha' class='form-control mb-2'><select name='cargo' class='form-select mb-2'><option>Administrador</option><option>Recepção</option></select><button class='btn btn-dark'>Criar</button></form>"))

# ... demais funções vazias seriam mantidas aqui.
