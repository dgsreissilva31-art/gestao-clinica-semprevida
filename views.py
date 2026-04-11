import datetime, urllib.parse, re
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render




# --- FUNÇÃO PARA PEGAR CARGO ---
def get_cargo(user):
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT cargo 
            FROM perfis_usuario 
            WHERE user_id = %s
        """, [user.id])

        resultado = cursor.fetchone()

    return resultado[0] if resultado else None


# --- DECORATOR DE PERMISSÃO ---
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



def cargo_required(cargo_necessario):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT cargo FROM perfis_usuario WHERE user_id = %s
                """, [request.user.id])
                resultado = cursor.fetchone()

            if not resultado:
                return HttpResponse("Usuário sem perfil", status=403)

            cargo_usuario = resultado[0]

            if cargo_usuario != cargo_necessario:
                return HttpResponse("Acesso negado", status=403)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


















# --- 1. TEMPLATE BASE ---

def base_html(titulo, conteudo):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <title>{titulo} - Grupo Sempre Vida</title>
        <style>
            :root {{ --sidebar-width: 260px; --top-bg: #3c8dbc; --sidebar-bg: #222d32; }}
            body {{ background-color: #ecf0f5; font-family: 'Segoe UI', sans-serif; margin: 0; overflow-x: hidden; }}
            .navbar-top {{ background-color: var(--top-bg); height: 50px; position: fixed; width: 100%; top: 0; z-index: 1000; color: white; display: flex; align-items: center; padding: 0 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .sidebar {{ background-color: var(--sidebar-bg); width: var(--sidebar-width); height: 100vh; position: fixed; top: 0; left: 0; padding-top: 50px; z-index: 999; overflow-y: auto; transition: all 0.3s; }}
            .sidebar-menu {{ list-style: none; padding: 0; margin: 0; }}
            .sidebar-menu li a {{ padding: 10px 15px; display: flex; align-items: center; color: #b8c7ce; text-decoration: none; border-left: 3px solid transparent; font-size: 14px; }}
            .sidebar-menu li a:hover {{ background: #1e282c; color: white; border-left-color: #3c8dbc; }}
            .menu-label {{ padding: 12px 15px 5px; font-size: 11px; color: #4b646f; background: #1a2226; text-transform: uppercase; font-weight: bold; }}
            .main-content {{ margin-left: var(--sidebar-width); padding: 70px 20px 20px; min-height: 100vh; }}
            .card-panel {{ background: white; border-top: 3px solid #3c8dbc; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 20px; }}
            @media (max-width: 768px) {{ .sidebar {{ left: -260px; }} .main-content {{ margin-left: 0; }} .sidebar.active {{ left: 0; }} }}
        </style>
    </head>
    <body>
        <div class="navbar-top d-flex justify-content-between">
            <div>
                <i class="bi bi-list fs-4" style="cursor:pointer" onclick="document.querySelector('.sidebar').classList.toggle('active')"></i> 
                <span class="ms-2 fw-bold text-uppercase">SEMPRE VIDA</span>
            </div>
            <div class="small">
                <i class="bi bi-person-circle"></i> Douglas Silva | 
                <a href="/logout/" class="text-white ms-2 text-decoration-none"><i class="bi bi-box-arrow-right"></i> Sair</a>
            </div>
        </div>
        <div class="sidebar shadow">
            <ul class="sidebar-menu">
                <div class="menu-label">Principal</div>
                <li><a href="/admin-painel/"><i class="bi bi-speedometer2"></i> Dashboard</a></li>
                <div class="menu-label">Operacional</div>
                <li><a href="/recepcao/"><i class="bi bi-person-check-fill"></i> Recepção</a></li>
                <li><a href="/agendar/"><i class="bi bi-calendar-plus-fill"></i> Novo Agendamento</a></li>
                <li><a href="/caixa/"><i class="bi bi-cash-stack"></i> Caixa do Dia</a></li>
                <li><a href="/agenda-diaria/"><i class="bi bi-calendar3"></i> Agenda Geral</a></li>
                <div class="menu-label">Cadastros</div>
                <li><a href="/pacientes/"><i class="bi bi-people-fill"></i> Pacientes</a></li>
                <li><a href="/profissionais/"><i class="bi bi-person-badge"></i> Profissionais</a></li>
                <li><a href="/unidades/"><i class="bi bi-building"></i> Unidades</a></li>
                <li><a href="/especialidades/"><i class="bi bi-hospital"></i> Especialidades</a></li>
                <div class="menu-label">Configurações</div>
                <li><a href="/acessos/"><i class="bi bi-shield-lock-fill"></i> Acessos</a></li>
                <li><a href="/precos/"><i class="bi bi-currency-dollar"></i> Preços</a></li>
            </ul>
        </div>
        <div class="main-content"><div class="card-panel">{conteudo}</div></div>
    </body>
    </html>
    """

# --- 2. LOGIN / LOGOUT (SEM DECORADOR) ---

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

# --- 3. VIEWS PROTEGIDAS (@login_required) ---

@login_required
def painel_controle(request):
    conteudo = """
        <div class="mb-4">
            <h3 class="fw-bold text-dark"><i class="bi bi-speedometer2 text-primary"></i> Painel de Gestão</h3>
            <p class="text-muted">Bem-vindo ao sistema de controle clínico Sempre Vida.</p>
        </div>
        <div class="row g-3">
            <div class="col-md-4"><div class="p-4 bg-primary text-white rounded shadow-sm text-center">
                <i class="bi bi-calendar-plus fs-1"></i><br><h5 class="mt-2">Novo Agendamento</h5><a href="/agendar/" class="btn btn-sm btn-light w-100 mt-2">Iniciar</a>
            </div></div>
            <div class="col-md-4"><div class="p-4 bg-success text-white rounded shadow-sm text-center">
                <i class="bi bi-person-check fs-1"></i><br><h5 class="mt-2">Recepção / Check-in</h5><a href="/recepcao/" class="btn btn-sm btn-light w-100 mt-2">Abrir</a>
            </div></div>
            <div class="col-md-4"><div class="p-4 bg-warning text-dark rounded shadow-sm text-center">
                <i class="bi bi-cash-stack fs-1"></i><br><h5 class="mt-2">Caixa do Dia</h5><a href="/caixa/" class="btn btn-sm btn-dark w-100 mt-2">Ver Saldo</a>
            </div></div>
        </div>
    """
    return HttpResponse(base_html("Dashboard", conteudo))





# 🔒 DECORATOR CORRIGIDO
def cargo_required(cargo_necessario):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return HttpResponse("❌ Usuário não autenticado", status=403)

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT cargo 
                    FROM perfis_usuario 
                    WHERE user_id = %s
                """, [request.user.id])

                resultado = cursor.fetchone()

            if not resultado:
                return HttpResponse("❌ Usuário sem perfil cadastrado", status=403)

            cargo_usuario = str(resultado[0]).strip().lower()
            cargo_necessario_fmt = str(cargo_necessario).strip().lower()

            if cargo_usuario != cargo_necessario_fmt:
                return HttpResponse("❌ Acesso negado: somente Administrador", status=403)

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator


# --- CADASTRO DE UNIDADES (INALTERADO + PROTEÇÃO REAL) ---

@cargo_required('Administrador')
@login_required
def cadastro_unidade(request):
    mensagem = ""
    edit_id = request.GET.get('edit')
    unidade_data = [None, "", "", ""] 

    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, nome, endereco, telefone FROM unidades WHERE id = %s",
                [edit_id]
            )
            unidade_data = cursor.fetchone() or unidade_data

    if request.method == "POST":
        id_post = request.POST.get('id_unidade')
        nome = request.POST.get('nome')
        end = request.POST.get('endereco')
        tel = request.POST.get('telefone')

        with connection.cursor() as cursor:
            if id_post:
                cursor.execute(
                    "UPDATE unidades SET nome=%s, endereco=%s, telefone=%s WHERE id=%s",
                    [nome, end, tel, id_post]
                )
            else:
                cursor.execute(
                    "INSERT INTO unidades (nome, endereco, telefone) VALUES (%s, %s, %s)",
                    [nome, end, tel]
                )

        return HttpResponseRedirect('/unidades/lista/')

    conteudo = f"""
        <h4>Unidade</h4>
        <form method='POST' class='row g-3'>
            <input type='hidden' name='id_unidade' value='{unidade_data[0] or ''}'>

            <div class='col-md-6'>
                <label>Nome</label>
                <input type='text' name='nome' class='form-control' value='{unidade_data[1]}' required>
            </div>

            <div class='col-md-6'>
                <label>Endereço</label>
                <input type='text' name='endereco' class='form-control' value='{unidade_data[2]}'>
            </div>

            <div class='col-md-6'>
                <label>Telefone</label>
                <input type='text' name='telefone' class='form-control' value='{unidade_data[3]}'>
            </div>

            <div class='col-12'>
                <button type='submit' class='btn btn-primary'>Salvar</button>
            </div>
        </form>
    """

    return HttpResponse(base_html("Unidades", conteudo))








@login_required
def lista_unidades(request):
    if request.GET.get('delete'):
        with connection.cursor() as cursor: cursor.execute("DELETE FROM unidades WHERE id = %s", [request.GET.get('delete')])
        return HttpResponseRedirect('/unidades/lista/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, endereco, telefone FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()
    linhas = "".join([f"<tr><td>{u[1]}</td><td><a href='/unidades/?edit={u[0]}' class='btn btn-sm btn-info text-white'>Editar</a></td></tr>" for u in unidades])
    return HttpResponse(base_html("Lista", f"<table class='table'>{linhas}</table>"))

@login_required
@csrf_exempt
def especialidades_geral(request):
    if request.GET.get('delete_esp'):
        with connection.cursor() as cursor: cursor.execute("DELETE FROM especialidades WHERE id = %s", [request.GET.get('delete_esp')])
        return HttpResponseRedirect('/especialidades/')
    if request.method == "POST":
        nome, tipo = request.POST.get('nome'), request.POST.get('tipo')
        with connection.cursor() as cursor: cursor.execute("INSERT INTO especialidades (nome, tipo) VALUES (%s, %s)", [nome, tipo])
        return HttpResponseRedirect('/especialidades/')
    return HttpResponse(base_html("Especialidades", "<h4>Especialidades</h4><form method='POST'><input name='nome' class='form-control mb-2' required><button class='btn btn-primary'>Salvar</button></form>"))

@login_required
@csrf_exempt
def profissionais_geral(request):
    if request.method == "POST":
        nome, num, esp = request.POST.get('nome'), request.POST.get('numero'), request.POST.get('especialidade_id')
        unid = request.POST.get('unidade_id')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO profissionais (nome, conselho_numero, especialidade_id, unidade_id) VALUES (%s,%s,%s,%s)", [nome, num, esp, unid])
        return HttpResponseRedirect('/profissionais/')
    return HttpResponse(base_html("Profissionais", "<h4>Cadastro de Profissionais</h4><form method='POST'><input name='nome' placeholder='Nome' class='form-control mb-2'><button class='btn btn-primary'>Salvar</button></form>"))

@login_required
@csrf_exempt
def pacientes_geral(request):
    termo = request.GET.get('busca', '')
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, cpf, telefone FROM pacientes WHERE nome ILIKE %s ORDER BY id DESC", [f'%{termo}%'])
        pacs = cursor.fetchall()
    linhas = "".join([f"<tr><td>{p[1]}</td><td>{p[2]}</td></tr>" for p in pacs])
    return HttpResponse(base_html("Pacientes", f"<h4>Pacientes</h4><table class='table'>{linhas}</table>"))

@login_required
@csrf_exempt
def recepcao_geral(request):
    data_hoje = datetime.date.today()
    unidade_filtro = request.GET.get('unidade', '')
    with connection.cursor() as cursor:
        sql = "SELECT ag.id, pac.nome, prof.nome, ag.horario_selecionado, ag.status FROM agendamentos ag JOIN pacientes pac ON ag.paciente_id = pac.id JOIN agendas_config ac ON ag.agenda_config_id = ac.id JOIN profissionais prof ON ac.profissional_id = prof.id WHERE ag.data_agendamento = %s"
        cursor.execute(sql, [data_hoje])
        agenda = cursor.fetchall()
    linhas = "".join([f"<tr><td>{a[3]}</td><td>{a[1]}</td><td><a href='/recepcao/?fluxo_id={a[0]}&etapa=2' class='btn btn-warning btn-sm'>Check-in</a></td></tr>" for a in agenda])
    return HttpResponse(base_html("Recepção", f"<table class='table'>{linhas}</table>"))

@login_required
@csrf_exempt
def prontuario_geral(request):
    ag_id = request.GET.get('id')
    if request.method == "POST":
        queixa, diag = request.POST.get('queixa'), request.POST.get('diagnostico')
        with connection.cursor() as cursor:
            cursor.execute("UPDATE agendamentos SET status = 'Finalizado' WHERE id = %s", [ag_id])
        return HttpResponseRedirect('/recepcao/')
    return HttpResponse(base_html("Prontuário", "<h4>Atendimento</h4><form method='POST'><textarea name='queixa' class='form-control mb-2'></textarea><button class='btn btn-primary'>Salvar</button></form>"))

@login_required
def caixa_geral(request):
    hoje = datetime.date.today()
    with connection.cursor() as cursor:
        cursor.execute("SELECT paciente_nome, valor, forma_pagamento FROM caixa WHERE data_pagamento = %s", [hoje])
        movs = cursor.fetchall()
    total = sum([float(m[1]) for m in movs])
    return HttpResponse(base_html("Caixa", f"<h3>Total: R$ {total:.2f}</h3>"))

@login_required
@csrf_exempt
def acesso_geral(request):
    User = get_user_model()
    if request.method == "POST":
        nome, user, senha, cargo, cpf = request.POST.get('nome'), request.POST.get('username'), request.POST.get('senha'), request.POST.get('cargo'), request.POST.get('cpf')
        if not User.objects.filter(username=user).exists():
            u_obj = User.objects.create_user(username=user, password=senha)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO perfis_usuario (user_id, nome_completo, cargo, cpf) VALUES (%s,%s,%s,%s)", [u_obj.id, nome, cargo, cpf])
        return HttpResponseRedirect('/acessos/')
    return HttpResponse(base_html("Acessos", "<h4>Acessos</h4><form method='POST'><input name='username' placeholder='Usuário' class='form-control mb-2'><button class='btn btn-dark'>Criar</button></form>"))

@login_required
@csrf_exempt
def agendar_consulta(request):
    # Lógica de novo agendamento...
    return HttpResponse(base_html("Agendar", "<h4>Novo Agendamento</h4><p>Selecione os dados para marcar a consulta.</p>"))

@login_required
def agenda_diaria(request):
    # Lógica de visualização da agenda geral...
    return HttpResponse(base_html("Agenda Geral", "<h4>Agenda Diária</h4>"))

@login_required
@csrf_exempt
def convenios_geral(request):
    return HttpResponse(base_html("Convênios", "<h4>Gestão de Convênios</h4>"))

@login_required
@csrf_exempt
def exames_geral(request):
    return HttpResponse(base_html("Exames", "<h4>Gestão de Exames</h4>"))

@login_required
@csrf_exempt
def odonto_geral(request):
    return HttpResponse(base_html("Odontologia", "<h4>Procedimentos Odontológicos</h4>"))

@login_required
@csrf_exempt
def precos_geral(request):
    return HttpResponse(base_html("Preços", "<h4>Tabela de Preços</h4>"))

@login_required
@csrf_exempt
def precos_exames_geral(request):
    return HttpResponse(base_html("Preços Exames", "<h4>Preços de Exames</h4>"))

@login_required
@csrf_exempt
def agendas_config_geral(request):
    return HttpResponse(base_html("Config Grade", "<h4>Configurar Grades de Horário</h4>"))

