import datetime
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# --- 1. TEMPLATE BASE ADMINISTRATIVO ---

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
            body {{ background-color: #ecf0f5; font-family: 'Segoe UI', sans-serif; margin: 0; }}
            .navbar-top {{ background-color: var(--top-bg); height: 50px; position: fixed; width: 100%; top: 0; z-index: 1000; color: white; display: flex; align-items: center; padding: 0 15px; }}
            .sidebar {{ background-color: var(--sidebar-bg); width: var(--sidebar-width); height: 100vh; position: fixed; top: 0; left: 0; padding-top: 50px; z-index: 999; }}
            .sidebar-menu {{ list-style: none; padding: 0; margin: 0; }}
            .sidebar-menu li a {{ padding: 12px 15px; display: block; color: #b8c7ce; text-decoration: none; border-left: 3px solid transparent; }}
            .sidebar-menu li a:hover {{ background: #1e282c; color: white; border-left-color: #3c8dbc; }}
            .menu-label {{ padding: 10px 15px; font-size: 12px; color: #4b646f; background: #1a2226; text-transform: uppercase; }}
            .main-content {{ margin-left: var(--sidebar-width); padding: 70px 20px 20px; }}
            .card-panel {{ background: white; border-top: 3px solid #d2d6de; border-radius: 3px; box-shadow: 0 1px 1px rgba(0,0,0,0.1); padding: 20px; }}
            @media (max-width: 768px) {{ .sidebar {{ left: -250px; }} .main-content {{ margin-left: 0; }} .sidebar.active {{ left: 0; }} }}
        </style>
    </head>
    <body>
        <div class="navbar-top d-flex justify-content-between">
            <div><i class="bi bi-list fs-4" style="cursor:pointer" onclick="document.querySelector('.sidebar').classList.toggle('active')"></i> <span class="ms-2 fw-bold text-uppercase">SEMPRE VIDA</span></div>
            <div><i class="bi bi-person-circle"></i> Douglas Silva</div>
        </div>
        <div class="sidebar">
            <ul class="sidebar-menu">
                <div class="menu-label">Navegação</div>
                <li><a href="/admin-painel/"><i class="bi bi-speedometer2"></i> Dashboard</a></li>
                <div class="menu-label">Administrativo</div>
                <li><a href="/unidades/"><i class="bi bi-building"></i> Unidades</a></li>
                <li><a href="/especialidades/"><i class="bi bi-hospital"></i> Especialidades</a></li>
                <li><a href="/profissionais/"><i class="bi bi-person-badge"></i> Profissionais</a></li>
                <li><a href="/convenios/"><i class="bi bi-card-checklist"></i> Convênios</a></li>
                <li><a href="/exames/"><i class="bi bi-microscope"></i> Exames</a></li>
                <li><a href="/odontologia/"><i class="bi bi-mask"></i> Odontologia</a></li>
                <li><a href="/pacientes/"><i class="bi bi-people"></i> Pacientes</a></li>
                <li><a href="/acessos/"><i class="bi bi-shield-lock"></i> Acessos</a></li>
                <li><a href="/precos/"><i class="bi bi-currency-dollar"></i> Preços Convênio</a></li>
                <li><a href="/precos-exames/"><i class="bi bi-tags"></i> Preços Exames</a></li>
                <li><a href="/agendas-config/"><i class="bi bi-calendar-check"></i> Configurar Agendas</a></li>
                <hr>
                <li><a href="/" class="text-info"><i class="bi bi-globe"></i> Ver Site Público</a></li>
            </ul>
        </div>
        <div class="main-content">
            <div class="card-panel">{conteudo}</div>
        </div>
    </body>
    </html>
    """

# --- 2. TELA 12: AGENDAMENTO PÚBLICO (ABERTURA) ---

@csrf_exempt
def marcar_consulta_publico(request):
    mensagem = ""
    unid = request.GET.get('unidade', '')
    espec = request.GET.get('especialidade', '')
    data_sel = request.GET.get('data', '')

    if request.method == "POST":
        ag_id = request.POST.get('agenda_id')
        hora = request.POST.get('horario')
        dt_f = request.POST.get('data_f')
        if ag_id and hora and dt_f:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO agendamentos (agenda_config_id, data_agendamento, horario_selecionado) VALUES (%s, %s, %s)", [ag_id, dt_f, hora])
                return HttpResponse("<html><meta charset='utf-8'><script>alert('Sucesso!'); window.location.href='/';</script></html>")
            except Exception as e:
                mensagem = f"<div class='alert alert-danger'>Erro: {e}</div>"

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        lista_unid = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM especialidades ORDER BY nome")
        lista_espec = cursor.fetchall()
        grade = []
        if unid and espec and data_sel:
            try:
                ano, mes, dia = map(int, data_sel.split('-'))
                d_obj = datetime.date(ano, mes, dia)
                dias = {0:'Segunda-feira', 1:'Terça-feira', 2:'Quarta-feira', 3:'Quinta-feira', 4:'Sexta-feira', 5:'Sábado', 6:'Domingo'}
                cursor.execute("""SELECT ac.id, p.nome, ac.horario_inicio FROM agendas_config ac JOIN profissionais p ON ac.profissional_id = p.id WHERE ac.unidade_id = %s AND ac.especialidade_id = %s AND (ac.dia_semana = %s OR ac.data_especifica = %s)""", [unid, espec, dias.get(d_obj.weekday()), data_sel])
                grade = cursor.fetchall()
            except: pass

    opts_u = "".join([f'<option value="{u[0]}" {"selected" if str(u[0])==unid else ""}>{u[1]}</option>' for u in lista_unid])
    opts_e = "".join([f'<option value="{e[0]}" {"selected" if str(e[0])==espec else ""}>{e[1]}</option>' for e in lista_espec])
    opts_h = "".join([f'<option value="{g[0]}|{g[2]}">{g[1]} - {g[2]}</option>' for g in grade])

    return HttpResponse(f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><title>Sempre Vida</title></head>
    <body style="background: linear-gradient(135deg, #3c8dbc, #1e282c); min-height: 100vh; padding: 20px;">
        <div class="card mx-auto mt-4 p-4 shadow-lg" style="max-width: 500px; border-radius: 20px;">
            <h3 class="text-center text-primary fw-bold">SEMPRE VIDA</h3>
            {mensagem}
            <form method="GET" class="row g-2">
                <div class="col-12"><label class="small fw-bold">Unidade</label><select name="unidade" class="form-select" onchange="this.form.submit()"><option value="">Onde?</option>{opts_u}</select></div>
                <div class="col-6"><label class="small fw-bold">Especialidade</label><select name="especialidade" class="form-select" onchange="this.form.submit()"><option value="">Médico?</option>{opts_e}</select></div>
                <div class="col-6"><label class="small fw-bold">Data</label><input type="date" name="data" class="form-control" value="{data_sel}" onchange="this.form.submit()"></div>
            </form>
            <hr>
            <form method="POST">
                <select name="h_full" class="form-select mb-3" required onchange="var d=this.value.split('|'); document.getElementById('ag').value=d[0]; document.getElementById('ho').value=d[1];"><option value="">{ 'Selecione o horário' if grade else 'Sem vagas' }</option>{opts_h}</select>
                <input type="hidden" name="agenda_id" id="ag"><input type="hidden" name="horario" id="ho"><input type="hidden" name="data_f" value="{data_sel}">
                <input type="text" name="paciente_nome" class="form-control mb-2" placeholder="Seu Nome" required>
                <button type="submit" class="btn btn-primary w-100 fw-bold rounded-pill">AGENDAR CONSULTA</button>
                <div class="text-center mt-3"><a href="/admin-painel/" class="text-muted small">Painel Admin</a></div>
            </form>
        </div>
    </body></html>""")

# --- 3. PAINEL ADMINISTRATIVO ---

def painel_controle(request):
    conteudo = """
        <div class="row g-3">
            <div class="col-md-4"><div class="p-4 bg-primary text-white rounded shadow-sm text-center"><h5>Unidades</h5><a href="/unidades/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a></div></div>
            <div class="col-md-4"><div class="p-4 bg-success text-white rounded shadow-sm text-center"><h5>Especialidades</h5><a href="/especialidades/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a></div></div>
            <div class="col-md-4"><div class="p-4 bg-danger text-white rounded shadow-sm text-center"><h5>Pacientes</h5><a href="/pacientes/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a></div></div>
            <div class="col-md-4"><div class="p-4 bg-dark text-white rounded shadow-sm text-center"><h5>Acessos</h5><a href="/acessos/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a></div></div>
            <div class="col-md-4"><div class="p-4 bg-info text-white rounded shadow-sm text-center"><h5>Config. Agendas</h5><a href="/agendas-config/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a></div></div>
        </div>"""
    return HttpResponse(base_html("Dashboard", conteudo))

# --- 4. FUNÇÕES ADMINISTRATIVAS (SIMPLIFICADAS PARA EVITAR ERROS) ---

@csrf_exempt
def cadastro_unidade(request):
    if request.method == "POST":
        nome, tel = request.POST.get('nome'), request.POST.get('telefone')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO unidades (nome, telefone) VALUES (%s, %s)", [nome, tel])
        return HttpResponseRedirect('/unidades/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, telefone FROM unidades ORDER BY nome")
        unids = cursor.fetchall()
    linhas = "".join([f"<tr><td>{u[1]}</td><td>{u[2]}</td></tr>" for u in unids])
    conteudo = f"<h4>Unidades</h4><form method='POST' class='row g-2 mb-4'><div class='col-6'><input type='text' name='nome' class='form-control' placeholder='Nome' required></div><div class='col-4'><input type='text' name='telefone' class='form-control' placeholder='Tel'></div><div class='col-2'><button class='btn btn-primary w-100'>+</button></div></form><table class='table'><thead><tr><th>Nome</th><th>Tel</th></tr></thead><tbody>{linhas}</tbody></table>"
    return HttpResponse(base_html("Unidades", conteudo))

@csrf_exempt
def especialidades_geral(request):
    if request.method == "POST":
        nome, tipo = request.POST.get('nome'), request.POST.get('tipo')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO especialidades (nome, tipo) VALUES (%s, %s)", [nome, tipo])
        return HttpResponseRedirect('/especialidades/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, tipo FROM especialidades ORDER BY nome")
        esps = cursor.fetchall()
    linhas = "".join([f"<tr><td>{e[0]}</td><td>{e[1]}</td></tr>" for e in esps])
    conteudo = f"<h4>Especialidades</h4><form method='POST' class='row g-2 mb-4'><div class='col-6'><input type='text' name='nome' class='form-control' required></div><div class='col-4'><select name='tipo' class='form-select'><option value='Médica'>Médica</option><option value='Odontológica'>Odontológica</option></select></div><div class='col-2'><button class='btn btn-success w-100'>+</button></div></form><table class='table'><tbody>{linhas}</tbody></table>"
    return HttpResponse(base_html("Especialidades", conteudo))

@csrf_exempt
def profissionais_geral(request):
    if request.method == "POST":
        nome, num, esp = request.POST.get('nome'), request.POST.get('numero'), request.POST.get('esp_id')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO profissionais (nome, conselho_numero, especialidade_id) VALUES (%s, %s, %s)", [nome, num, esp])
        return HttpResponseRedirect('/profissionais/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM especialidades")
        esps = cursor.fetchall()
        cursor.execute("SELECT p.nome, e.nome FROM profissionais p JOIN especialidades e ON p.especialidade_id = e.id")
        profs = cursor.fetchall()
    opts = "".join([f"<option value='{e[0]}'>{e[1]}</option>" for e in esps])
    linhas = "".join([f"<tr><td>{p[0]}</td><td>{p[1]}</td></tr>" for p in profs])
    conteudo = f"<h4>Profissionais</h4><form method='POST' class='row g-2 mb-4'><div class='col-4'><input name='nome' class='form-control' placeholder='Nome'></div><div class='col-3'><input name='numero' class='form-control' placeholder='Registro'></div><div class='col-3'><select name='esp_id' class='form-select'>{opts}</select></div><div class='col-2'><button class='btn btn-warning w-100'>+</button></div></form><table class='table'><tbody>{linhas}</tbody></table>"
    return HttpResponse(base_html("Profissionais", conteudo))

@csrf_exempt
def convenios_geral(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO convenios (nome) VALUES (%s)", [nome])
        return HttpResponseRedirect('/convenios/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome FROM convenios")
        convs = cursor.fetchall()
    linhas = "".join([f"<tr><td>{c[0]}</td></tr>" for c in convs])
    conteudo = f"<h4>Convênios</h4><form method='POST' class='d-flex gap-2 mb-3'><input name='nome' class='form-control'><button class='btn btn-info'>+</button></form><table class='table'><tbody>{linhas}</tbody></table>"
    return HttpResponse(base_html("Convênios", conteudo))

@csrf_exempt
def exames_geral(request):
    if request.method == "POST":
        nome, grupo = request.POST.get('nome'), request.POST.get('grupo')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO exames (nome, grupo) VALUES (%s, %s)", [nome, grupo])
        return HttpResponseRedirect('/exames/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, grupo FROM exames")
        exs = cursor.fetchall()
    linhas = "".join([f"<tr><td>{x[0]}</td><td>{x[1]}</td></tr>" for x in exs])
    conteudo = f"<h4>Exames</h4><form method='POST' class='row g-2 mb-3'><div class='col-6'><input name='nome' class='form-control'></div><div class='col-4'><input name='grupo' class='form-control'></div><button class='btn btn-secondary col-2'>+</button></form><table class='table'><tbody>{linhas}</tbody></table>"
    return HttpResponse(base_html("Exames", conteudo))

@csrf_exempt
def odonto_geral(request):
    if request.method == "POST":
        proc = request.POST.get('proc')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO odontologia (procedimento) VALUES (%s)", [proc])
        return HttpResponseRedirect('/odontologia/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT procedimento FROM odontologia")
        ods = cursor.fetchall()
    linhas = "".join([f"<tr><td>{o[0]}</td></tr>" for o in ods])
    conteudo = f"<h4>Odonto</h4><form method='POST' class='d-flex gap-2 mb-3'><input name='proc' class='form-control'><button class='btn btn-dark'>+</button></form><table class='table'><tbody>{linhas}</tbody></table>"
    return HttpResponse(base_html("Odonto", conteudo))

@csrf_exempt
def pacientes_geral(request):
    if request.method == "POST":
        nome, cpf = request.POST.get('nome'), request.POST.get('cpf')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO pacientes (nome, cpf) VALUES (%s, %s)", [nome, cpf])
        return HttpResponseRedirect('/pacientes/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome, cpf FROM pacientes")
        pacs = cursor.fetchall()
    linhas = "".join([f"<tr><td>{p[0]}</td><td>{p[1]}</td></tr>" for p in pacs])
    conteudo = f"<h4>Pacientes</h4><form method='POST' class='row g-2 mb-3'><div class='col-6'><input name='nome' class='form-control'></div><div class='col-4'><input name='cpf' class='form-control'></div><button class='btn btn-danger col-2'>+</button></form><table class='table'><tbody>{linhas}</tbody></table>"
    return HttpResponse(base_html("Pacientes", conteudo))

@csrf_exempt
def acesso_geral(request):
    if request.method == "POST":
        user, senha = request.POST.get('user'), request.POST.get('pass')
        User.objects.create_user(username=user, password=senha)
        return HttpResponseRedirect('/acessos/')
    users = User.objects.all()
    linhas = "".join([f"<tr><td>{u.username}</td></tr>" for u in users])
    conteudo = f"<h4>Acessos</h4><form method='POST' class='row g-2 mb-3'><div class='col-5'><input name='user' class='form-control' placeholder='Login'></div><div class='col-5'><input name='pass' type='password' class='form-control' placeholder='Senha'></div><button class='btn btn-dark col-2'>+</button></form><table class='table'><tbody>{linhas}</tbody></table>"
    return HttpResponse(base_html("Acessos", conteudo))

@csrf_exempt
def precos_geral(request):
    return HttpResponse(base_html("Preços", "<h4>Tabela de Preços</h4><p>Funcionalidade em desenvolvimento.</p>"))

@csrf_exempt
def precos_exames_geral(request):
    return HttpResponse(base_html("Preços Exames", "<h4>Tabela de Exames</h4><p>Funcionalidade em desenvolvimento.</p>"))

@csrf_exempt
def agendas_config_geral(request):
    if request.method == "POST":
        prof, unid, esp, dia, inicio, fim = request.POST.get('p'), request.POST.get('u'), request.POST.get('e'), request.POST.get('d'), request.POST.get('i'), request.POST.get('f')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO agendas_config (profissional_id, unidade_id, especialidade_id, dia_semana, horario_inicio, horario_fim) VALUES (%s, %s, %s, %s, %s, %s)", [prof, unid, esp, dia, inicio, fim])
        return HttpResponseRedirect('/agendas-config/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM profissionais")
        ps = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM unidades")
        us = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM especialidades")
        es = cursor.fetchall()
    opt_p = "".join([f"<option value='{x[0]}'>{x[1]}</option>" for x in ps])
    opt_u = "".join([f"<option value='{x[0]}'>{x[1]}</option>" for x in us])
    opt_e = "".join([f"<option value='{x[0]}'>{x[1]}</option>" for x in es])
    conteudo = f"<h4>Configurar Agenda</h4><form method='POST' class='row g-2'><select name='p' class='col-md-4 form-select'>{opt_p}</select><select name='u' class='col-md-4 form-select'>{opt_u}</select><select name='e' class='col-md-4 form-select'>{opt_e}</select><input name='d' class='form-control' placeholder='Segunda-feira'><input name='i' type='time' class='form-control'><input name='f' type='time' class='form-control'><button class='btn btn-success'>Salvar</button></form>"
    return HttpResponse(base_html("Agendas", conteudo))

# --- 5. ROTAS FINAIS (URLPATTERNS) ---

urlpatterns = [
    path('', marcar_consulta_publico),
    path('admin-painel/', painel_controle),
    path('unidades/', cadastro_unidade),
    path('especialidades/', especialidades_geral),
    path('profissionais/', profissionais_geral),
    path('convenios/', convenios_geral),
    path('exames/', exames_geral),
    path('odontologia/', odonto_geral),
    path('pacientes/', pacientes_geral),
    path('acessos/', acesso_geral),
    path('precos/', precos_geral),
    path('precos-exames/', precos_exames_geral),
    path('agendas-config/', agendas_config_geral),
]
