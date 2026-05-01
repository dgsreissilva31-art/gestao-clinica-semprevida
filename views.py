import datetime, urllib.parse, re
from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# --- FUNÇÃO BASE ---
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


# --- DECORATOR DE PERMISSÃO ---
from functools import wraps

def cargo_required(cargo_permitido):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseRedirect("/login/")
            with connection.cursor() as cursor:
                cursor.execute("SELECT cargo FROM perfis_usuario WHERE user_id = %s", [request.user.id])
                res = cursor.fetchone()
            if not res:
                return HttpResponse("Acesso negado")
            if res[0] != cargo_permitido:
                return HttpResponse("Acesso restrito")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# --- LOGIN / LOGOUT ---
@csrf_exempt
def login_view(request):
    mensagem = ""
    if request.method == "POST":
        u = request.POST.get("username", "").strip()
        s = request.POST.get("senha", "").strip()
        user = authenticate(username=u, password=s)
        if user:
            login(request, user)
            with connection.cursor() as cursor:
                cursor.execute("SELECT cargo FROM perfis_usuario WHERE user_id = %s", [user.id])
                res = cursor.fetchone()
            if res and res[0] == 'Médico':
                return HttpResponseRedirect("/medico/prontuario/")
            if res and res[0] == 'Dentista':
                return HttpResponseRedirect("/dentista/prontuario/")
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


# --- TELA EXCLUSIVA DO MÉDICO ---
@login_required
@cargo_required('Médico')
def prontuario_medico(request):
    data_hoje = datetime.date.today()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT prof.id, prof.nome
            FROM profissionais prof
            JOIN perfis_usuario pu ON pu.user_id = %s
            WHERE prof.nome = pu.nome_completo
            LIMIT 1
        """, [request.user.id])
        profissional = cursor.fetchone()

    if not profissional:
        return HttpResponse("""
            <!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head><body class="bg-light d-flex justify-content-center align-items-center" style="height:100vh;">
            <div class="text-center">
                <h3>⚠️ Profissional não encontrado</h3>
                <p class="text-muted">Seu usuário não está vinculado a nenhum profissional cadastrado.</p>
                <a href="/logout/" class="btn btn-danger">Sair</a>
            </div></body></html>
        """)

    prof_id, prof_nome = profissional

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ag.id, pac.nome, ag.horario_selecionado, ag.status, u.nome
            FROM agendamentos ag
            JOIN pacientes pac ON ag.paciente_id = pac.id
            JOIN agendas_config ac ON ag.agenda_config_id = ac.id
            JOIN unidades u ON ac.unidade_id = u.id
            WHERE ac.profissional_id = %s AND ag.data_agendamento = %s
            ORDER BY ag.horario_selecionado
        """, [prof_id, data_hoje])
        agenda = cursor.fetchall()

    linhas = ""
    for a in agenda:
        status = a[3] or "Agendado"
        if status == "Chegada":
            btn = f'<a href="/prontuario/?id={a[0]}" class="btn btn-success btn-sm"><i class="bi bi-clipboard2-pulse"></i> Prontuário</a>'
        elif status == "Agendado":
            btn = '<span class="badge bg-warning text-dark"><i class="bi bi-hourglass-split"></i> Aguardando Check-in</span>'
        else:
            btn = f'<span class="badge bg-secondary">{status}</span>'
        linhas += f"<tr><td class='fw-bold'>{str(a[2])[:5]}</td><td>{a[1]}</td><td><span class='badge bg-light text-dark border'>{a[4]}</span></td><td>{btn}</td></tr>"

    corpo = f"""
        {"<p class='text-muted mt-3'>Nenhum agendamento para hoje.</p>" if not agenda else f'''
        <table class="table table-hover align-middle mt-3">
            <thead class="table-light"><tr><th>Hora</th><th>Paciente</th><th>Unidade</th><th>Ação</th></tr></thead>
            <tbody>{linhas}</tbody>
        </table>'''}
    """

    return HttpResponse(f"""
    <!DOCTYPE html><html lang="pt-br">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <title>Painel do Médico - Sempre Vida</title>
        <style>
            body {{ background:#f0f4f8; font-family:'Segoe UI',sans-serif; }}
            .topbar {{ background:linear-gradient(135deg,#1a6b3c,#27ae60); color:white; padding:12px 24px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 6px rgba(0,0,0,0.2); position:fixed; width:100%; top:0; z-index:1000; }}
            .container-medico {{ max-width:900px; margin:80px auto 40px; background:white; border-radius:10px; box-shadow:0 2px 12px rgba(0,0,0,0.1); overflow:hidden; }}
            .cabecalho {{ background:linear-gradient(135deg,#1a6b3c,#27ae60); color:white; padding:24px 28px; }}
            .cabecalho h5 {{ margin:0; font-size:13px; opacity:0.8; text-transform:uppercase; letter-spacing:1px; }}
            .cabecalho h3 {{ margin:6px 0 0; font-size:24px; font-weight:700; }}
            .corpo {{ padding:24px 28px; }}
            .badge-data {{ background:#e8f5e9; color:#1a6b3c; padding:6px 16px; border-radius:20px; font-size:13px; font-weight:600; display:inline-block; border:1px solid #c8e6c9; }}
        </style>
    </head>
    <body>
        <div class="topbar">
            <div style="font-size:18px;font-weight:bold;"><i class="bi bi-heart-pulse-fill"></i> &nbsp;SEMPRE VIDA</div>
            <div style="font-size:13px;">
                <i class="bi bi-person-circle"></i> {prof_nome} &nbsp;|&nbsp;
                <a href="/logout/" class="text-white text-decoration-none"><i class="bi bi-box-arrow-right"></i> Sair</a>
            </div>
        </div>
        <div class="container-medico">
            <div class="cabecalho">
                <h5><i class="bi bi-calendar2-check"></i> Agenda do dia</h5>
                <h3>Dr(a). {prof_nome}</h3>
            </div>
            <div class="corpo">
                <div class="badge-data">📅 {data_hoje.strftime('%d/%m/%Y')}</div>
                {corpo}
            </div>
        </div>
    </body></html>
    """)


# --- TELA EXCLUSIVA DO DENTISTA ---
@login_required
@cargo_required('Dentista')
def prontuario_dentista_agenda(request):
    data_hoje = datetime.date.today()

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT prof.id, prof.nome
            FROM profissionais prof
            JOIN perfis_usuario pu ON pu.user_id = %s
            WHERE prof.nome = pu.nome_completo
            LIMIT 1
        """, [request.user.id])
        profissional = cursor.fetchone()

    if not profissional:
        return HttpResponse("""
            <!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            </head><body class="bg-light d-flex justify-content-center align-items-center" style="height:100vh;">
            <div class="text-center">
                <h3>⚠️ Profissional não encontrado</h3>
                <p class="text-muted">Seu usuário não está vinculado a nenhum profissional cadastrado.</p>
                <a href="/logout/" class="btn btn-danger">Sair</a>
            </div></body></html>
        """)

    prof_id, prof_nome = profissional

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ag.id, pac.nome, ag.horario_selecionado, ag.status, u.nome
            FROM agendamentos ag
            JOIN pacientes pac ON ag.paciente_id = pac.id
            JOIN agendas_config ac ON ag.agenda_config_id = ac.id
            JOIN unidades u ON ac.unidade_id = u.id
            WHERE ac.profissional_id = %s AND ag.data_agendamento = %s
            ORDER BY ag.horario_selecionado
        """, [prof_id, data_hoje])
        agenda = cursor.fetchall()

    linhas = ""
    for a in agenda:
        status = a[3] or "Agendado"
        if status == "Chegada":
            btn = f'<a href="/dentista/prontuario/atender/?id={a[0]}" class="btn btn-success btn-sm"><i class="bi bi-clipboard2-pulse"></i> Prontuário</a>'
        elif status == "Agendado":
            btn = '<span class="badge bg-warning text-dark"><i class="bi bi-hourglass-split"></i> Aguardando Check-in</span>'
        else:
            btn = f'<span class="badge bg-secondary">{status}</span>'
        linhas += f"<tr><td class='fw-bold'>{str(a[2])[:5]}</td><td>{a[1]}</td><td><span class='badge bg-light text-dark border'>{a[4]}</span></td><td>{btn}</td></tr>"

    corpo = f"""
        {"<p class='text-muted mt-3'>Nenhum agendamento para hoje.</p>" if not agenda else f'''
        <table class="table table-hover align-middle mt-3">
            <thead class="table-light"><tr><th>Hora</th><th>Paciente</th><th>Unidade</th><th>Ação</th></tr></thead>
            <tbody>{linhas}</tbody>
        </table>'''}
    """

    return HttpResponse(f"""
    <!DOCTYPE html><html lang="pt-br">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
        <title>Painel do Dentista - Sempre Vida</title>
        <style>
            body {{ background:#f0f4f8; font-family:'Segoe UI',sans-serif; }}
            .topbar {{ background:linear-gradient(135deg,#1a3a6b,#2e5ebc); color:white; padding:12px 24px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 6px rgba(0,0,0,0.2); position:fixed; width:100%; top:0; z-index:1000; }}
            .container-dentista {{ max-width:900px; margin:80px auto 40px; background:white; border-radius:10px; box-shadow:0 2px 12px rgba(0,0,0,0.1); overflow:hidden; }}
            .cabecalho {{ background:linear-gradient(135deg,#1a3a6b,#2e5ebc); color:white; padding:24px 28px; }}
            .cabecalho h5 {{ margin:0; font-size:13px; opacity:0.8; text-transform:uppercase; letter-spacing:1px; }}
            .cabecalho h3 {{ margin:6px 0 0; font-size:24px; font-weight:700; }}
            .corpo {{ padding:24px 28px; }}
            .badge-data {{ background:#e8edf5; color:#1a3a6b; padding:6px 16px; border-radius:20px; font-size:13px; font-weight:600; display:inline-block; border:1px solid #c8d4e6; }}
        </style>
    </head>
    <body>
        <div class="topbar">
            <div style="font-size:18px;font-weight:bold;"><i class="bi bi-mask"></i> &nbsp;SEMPRE VIDA</div>
            <div style="font-size:13px;">
                <i class="bi bi-person-circle"></i> {prof_nome} &nbsp;|&nbsp;
                <a href="/logout/" class="text-white text-decoration-none"><i class="bi bi-box-arrow-right"></i> Sair</a>
            </div>
        </div>
        <div class="container-dentista">
            <div class="cabecalho">
                <h5><i class="bi bi-calendar2-check"></i> Agenda do dia</h5>
                <h3>Dr(a). {prof_nome}</h3>
            </div>
            <div class="corpo">
                <div class="badge-data">📅 {data_hoje.strftime('%d/%m/%Y')}</div>
                {corpo}
            </div>
        </div>
    </body></html>
    """)


# --- PRONTUÁRIO MÉDICO ---
@csrf_exempt
def prontuario_geral(request):
    agendamento_id = request.GET.get('id')
    consultar = request.GET.get('consultar')
    busca = request.GET.get('busca') or ""
    ver = request.GET.get('ver')
    mensagem = ""

    with connection.cursor() as cursor:
        cursor.execute("SELECT cargo FROM perfis_usuario WHERE user_id = %s", [request.user.id])
        cargo_res = cursor.fetchone()
    cargo_atual = cargo_res[0] if cargo_res else ""
    is_medico = cargo_atual == "Médico"

    if not is_medico:
        return HttpResponse(base_html("Acesso Negado", """
            <div class="text-center py-5">
                <h3 class="text-danger">🔒 Acesso Restrito</h3>
                <p class="text-muted">Somente médicos podem acessar o prontuário.</p>
                <a href="/recepcao/" class="btn btn-primary">Voltar à Recepção</a>
            </div>
        """))

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT prof.id FROM profissionais prof
            JOIN perfis_usuario pu ON pu.user_id = %s
            WHERE prof.nome = pu.nome_completo LIMIT 1
        """, [request.user.id])
        prof_res = cursor.fetchone()
    prof_id_logado = prof_res[0] if prof_res else None

    def render_page(titulo, conteudo):
        return HttpResponse(f"""
        <!DOCTYPE html><html lang="pt-br">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
            <title>{titulo} - Sempre Vida</title>
            <style>
                body {{ background:#f0f4f8; font-family:'Segoe UI',sans-serif; }}
                .topbar {{ background:linear-gradient(135deg,#1a6b3c,#27ae60); color:white; padding:12px 24px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 6px rgba(0,0,0,0.2); position:fixed; width:100%; top:0; z-index:1000; }}
                .conteudo-medico {{ max-width:960px; margin:80px auto 40px; background:white; border-radius:10px; box-shadow:0 2px 12px rgba(0,0,0,0.1); padding:28px; }}
            </style>
        </head>
        <body>
            <div class="topbar">
                <div style="font-size:18px;font-weight:bold;"><i class="bi bi-heart-pulse-fill"></i> &nbsp;SEMPRE VIDA</div>
                <div style="font-size:13px;">
                    <i class="bi bi-person-circle"></i> {request.user.username} &nbsp;|&nbsp;
                    <a href="/medico/prontuario/" class="text-white text-decoration-none me-2"><i class="bi bi-arrow-left"></i> Agenda</a>
                    <a href="/logout/" class="text-white text-decoration-none"><i class="bi bi-box-arrow-right"></i> Sair</a>
                </div>
            </div>
            <div class="conteudo-medico">{conteudo}</div>
        </body></html>
        """)

    if ver:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.nome, pr.data_atendimento, prof.nome,
                       pr.queixa, pr.diagnostico, pr.procedimentos
                FROM prontuarios pr
                JOIN pacientes p ON pr.paciente_id = p.id
                JOIN profissionais prof ON pr.profissional_id = prof.id
                WHERE pr.id = %s AND pr.profissional_id = %s
            """, [ver, prof_id_logado])
            d = cursor.fetchone()
        if not d:
            return render_page("Erro", "Prontuário não encontrado.")
        data = d[1].strftime('%d/%m/%Y') if d[1] else ""
        conteudo = f"""
        <h4>📄 Prontuário Completo</h4>
        <a href="?consultar=1" class="btn btn-secondary mb-3">⬅ Voltar</a>
        <div class="card p-4 shadow-sm">
            <p><b>Paciente:</b> {d[0]}</p><p><b>Data:</b> {data}</p>
            <p><b>Médico:</b> {d[2]}</p><hr>
            <p><b>Histórico:</b><br><div style="white-space:pre-wrap;">{d[3]}</div></p>
            <p><b>Diagnóstico:</b><br><div style="white-space:pre-wrap;">{d[4]}</div></p>
            <p><b>Tratamento:</b><br><div style="white-space:pre-wrap;">{d[5]}</div></p>
        </div>"""
        return render_page("Prontuário Completo", conteudo)

    if consultar:
        with connection.cursor() as cursor:
            sql = """
                SELECT pr.id, p.nome, pr.data_atendimento, prof.nome,
                       pr.queixa, pr.diagnostico, pr.procedimentos
                FROM prontuarios pr
                JOIN pacientes p ON pr.paciente_id = p.id
                JOIN profissionais prof ON pr.profissional_id = prof.id
                WHERE pr.profissional_id = %s
            """
            params = [prof_id_logado]
            if busca:
                sql += " AND p.nome ILIKE %s"; params.append(f"%{busca}%")
            sql += " ORDER BY pr.data_atendimento DESC, p.nome ASC"
            cursor.execute(sql, params)
            dados = cursor.fetchall()

        linhas = "".join([f"""<tr>
            <td><b>{d[1]}</b></td><td>{d[2].strftime('%d/%m/%Y') if d[2] else ''}</td><td>{d[3]}</td>
            <td><div style='max-height:80px;overflow:auto;'>{d[4]}</div></td>
            <td><div style='max-height:80px;overflow:auto;'>{d[5]}</div></td>
            <td><div style='max-height:80px;overflow:auto;'>{d[6]}</div></td>
            <td><a href='?consultar=1&ver={d[0]}' class='btn btn-sm btn-primary'>Abrir Completo</a></td>
        </tr>""" for d in dados])

        conteudo = f"""
        <h4>📋 Prontuários</h4>
        <form method="GET" class="row mb-3">
            <input type="hidden" name="consultar" value="1">
            <div class="col-md-10"><input type="text" name="busca" value="{busca}" class="form-control" placeholder="Buscar por paciente..."></div>
            <div class="col-md-2"><button class="btn btn-primary w-100">Buscar</button></div>
        </form>
        <a href="/medico/prontuario/" class="btn btn-secondary mb-3">Voltar</a>
        <div style="overflow-x:auto;">
            <table class="table table-bordered table-hover">
                <thead class="table-dark"><tr><th>Paciente</th><th>Data</th><th>Médico</th><th>Histórico</th><th>Diagnóstico</th><th>Tratamento</th><th>Ação</th></tr></thead>
                <tbody>{linhas or '<tr><td colspan="7" class="text-center">Sem registros</td></tr>'}</tbody>
            </table>
        </div>"""
        return render_page("Consulta Prontuários", conteudo)

    if not agendamento_id:
        return render_page("Erro", "ID do agendamento não informado.")

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.nome, p.telefone, c.nome, pr.id, pr.nome,
                   ag.data_agendamento, ag.horario_selecionado
            FROM agendamentos ag
            JOIN pacientes p ON ag.paciente_id = p.id
            LEFT JOIN convenios c ON p.convenio_id = c.id
            JOIN agendas_config ac ON ag.agenda_config_id = ac.id
            JOIN profissionais pr ON ac.profissional_id = pr.id
            WHERE ag.id = %s
        """, [agendamento_id])
        dados = cursor.fetchone()
        if not dados:
            return render_page("Erro", "Agendamento não encontrado.")
        pac_id, pac_nome_bruto, pac_tel, conv_nome, prof_id, prof_nome, data, hora = dados
        pac_nome = pac_nome_bruto.split("(Ag:")[0].strip() if "(Ag:" in pac_nome_bruto else pac_nome_bruto

    if request.method == "POST":
        historico = request.POST.get('historico')
        diagnostico = request.POST.get('diagnostico')
        tratamento = request.POST.get('tratamento')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO prontuarios (paciente_id, profissional_id, data_atendimento, hora,
                     queixa, anamnese, diagnostico, procedimentos, observacoes)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, [pac_id, prof_id, data, hora, historico, historico, diagnostico, tratamento, ""])
                cursor.execute("UPDATE agendamentos SET status = 'Finalizado' WHERE id = %s", [agendamento_id])
            return HttpResponseRedirect('/medico/prontuario/')
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT data_atendimento, diagnostico, procedimentos, queixa
            FROM prontuarios WHERE paciente_id = %s AND profissional_id = %s
            ORDER BY data_atendimento DESC
        """, [pac_id, prof_id_logado])
        historico_lista = cursor.fetchall()

    lista_hist = "".join([f"""
        <div class='card mb-2 border-start border-primary border-4 shadow-sm'>
            <div class='card-body py-2'>
                <small class='fw-bold text-primary'>{h[0].strftime('%d/%m/%Y')}</small><br>
                <b>Histórico:</b> {h[3]}<br><b>Diagnóstico:</b> {h[1]}
            </div>
        </div>""" for h in historico_lista])

    conteudo = f"""
    <div class="container-fluid py-2">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4>Atendimento Profissional</h4>
            <div>
                <a href="?consultar=1" class="btn btn-info btn-sm me-2">📋 Consultar Prontuários</a>
                <a href="/medico/prontuario/" class="btn btn-outline-secondary btn-sm">Sair sem salvar</a>
            </div>
        </div>
        {mensagem}
        <div class="row">
            <div class="col-md-8">
                <div class="card p-3 mb-3"><b>Paciente:</b> {pac_nome}<br><b>Convênio:</b> {conv_nome or 'Particular'}</div>
                <form method="POST">
                    <label class="fw-bold">Histórico</label>
                    <textarea name="historico" class="form-control mb-2" rows="4" required></textarea>
                    <label class="fw-bold">Diagnóstico</label>
                    <textarea name="diagnostico" class="form-control mb-2" rows="3"></textarea>
                    <label class="fw-bold">Tratamento</label>
                    <textarea name="tratamento" class="form-control mb-3" rows="3"></textarea>
                    <button class="btn btn-primary w-100 fw-bold">Salvar Prontuário</button>
                </form>
            </div>
            <div class="col-md-4">
                <h6 class="fw-bold">Histórico do Paciente</h6>
                {lista_hist or '<p class="text-muted">Sem histórico</p>'}
            </div>
        </div>
    </div>"""
    return render_page("Prontuário", conteudo)


# --- PRONTUÁRIO ODONTOLÓGICO ---
@csrf_exempt
def prontuario_dentista(request):
    agendamento_id = request.GET.get('id')
    consultar = request.GET.get('consultar')
    busca = request.GET.get('busca') or ""
    ver = request.GET.get('ver')
    mensagem = ""

    with connection.cursor() as cursor:
        cursor.execute("SELECT cargo FROM perfis_usuario WHERE user_id = %s", [request.user.id])
        cargo_res = cursor.fetchone()
    cargo_atual = cargo_res[0] if cargo_res else ""
    is_dentista = cargo_atual == "Dentista"

    if not is_dentista:
        return HttpResponse(base_html("Acesso Negado", """
            <div class="text-center py-5">
                <h3 class="text-danger">🔒 Acesso Restrito</h3>
                <p class="text-muted">Somente dentistas podem acessar este prontuário.</p>
                <a href="/recepcao/" class="btn btn-primary">Voltar à Recepção</a>
            </div>
        """))

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT prof.id FROM profissionais prof
            JOIN perfis_usuario pu ON pu.user_id = %s
            WHERE prof.nome = pu.nome_completo LIMIT 1
        """, [request.user.id])
        prof_res = cursor.fetchone()
    prof_id_logado = prof_res[0] if prof_res else None

    def render_page(titulo, conteudo):
        return HttpResponse(f"""
        <!DOCTYPE html><html lang="pt-br">
        <head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
            <title>{titulo} - Sempre Vida</title>
            <style>
                body {{ background:#f0f4f8; font-family:'Segoe UI',sans-serif; }}
                .topbar {{ background:linear-gradient(135deg,#1a3a6b,#2e5ebc); color:white; padding:12px 24px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 6px rgba(0,0,0,0.2); position:fixed; width:100%; top:0; z-index:1000; }}
                .conteudo-dentista {{ max-width:960px; margin:80px auto 40px; background:white; border-radius:10px; box-shadow:0 2px 12px rgba(0,0,0,0.1); padding:28px; }}
            </style>
        </head>
        <body>
            <div class="topbar">
                <div style="font-size:18px;font-weight:bold;"><i class="bi bi-mask"></i> &nbsp;SEMPRE VIDA</div>
                <div style="font-size:13px;">
                    <i class="bi bi-person-circle"></i> {request.user.username} &nbsp;|&nbsp;
                    <a href="/dentista/prontuario/" class="text-white text-decoration-none me-2"><i class="bi bi-arrow-left"></i> Agenda</a>
                    <a href="/logout/" class="text-white text-decoration-none"><i class="bi bi-box-arrow-right"></i> Sair</a>
                </div>
            </div>
            <div class="conteudo-dentista">{conteudo}</div>
        </body></html>
        """)

    if ver:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.nome, po.data_atendimento, prof.nome,
                       po.queixa, po.diagnostico, po.procedimentos, po.dente, po.observacoes
                FROM prontuarios_odonto po
                JOIN pacientes p ON po.paciente_id = p.id
                JOIN profissionais prof ON po.profissional_id = prof.id
                WHERE po.id = %s AND po.profissional_id = %s
            """, [ver, prof_id_logado])
            d = cursor.fetchone()
        if not d:
            return render_page("Erro", "Prontuário não encontrado.")
        data = d[1].strftime('%d/%m/%Y') if d[1] else ""
        conteudo = f"""
        <h4>🦷 Prontuário Odontológico Completo</h4>
        <a href="?consultar=1" class="btn btn-secondary mb-3">⬅ Voltar</a>
        <div class="card p-4 shadow-sm">
            <p><b>Paciente:</b> {d[0]}</p><p><b>Data:</b> {data}</p>
            <p><b>Dentista:</b> {d[2]}</p><p><b>Dente(s):</b> {d[6] or '-'}</p><hr>
            <p><b>Queixa:</b><br><div style="white-space:pre-wrap;">{d[3]}</div></p>
            <p><b>Diagnóstico:</b><br><div style="white-space:pre-wrap;">{d[4]}</div></p>
            <p><b>Procedimento:</b><br><div style="white-space:pre-wrap;">{d[5]}</div></p>
            <p><b>Observações:</b><br><div style="white-space:pre-wrap;">{d[7]}</div></p>
        </div>"""
        return render_page("Prontuário Completo", conteudo)

    if consultar:
        with connection.cursor() as cursor:
            sql = """
                SELECT po.id, p.nome, po.data_atendimento, prof.nome,
                       po.queixa, po.diagnostico, po.procedimentos, po.dente
                FROM prontuarios_odonto po
                JOIN pacientes p ON po.paciente_id = p.id
                JOIN profissionais prof ON po.profissional_id = prof.id
                WHERE po.profissional_id = %s
            """
            params = [prof_id_logado]
            if busca:
                sql += " AND p.nome ILIKE %s"; params.append(f"%{busca}%")
            sql += " ORDER BY po.data_atendimento DESC, p.nome ASC"
            cursor.execute(sql, params)
            dados = cursor.fetchall()

        linhas = "".join([f"""<tr>
            <td><b>{d[1]}</b></td><td>{d[2].strftime('%d/%m/%Y') if d[2] else ''}</td>
            <td>{d[7] or '-'}</td>
            <td><div style='max-height:80px;overflow:auto;'>{d[4]}</div></td>
            <td><div style='max-height:80px;overflow:auto;'>{d[5]}</div></td>
            <td><div style='max-height:80px;overflow:auto;'>{d[6]}</div></td>
            <td><a href='?consultar=1&ver={d[0]}' class='btn btn-sm btn-primary'>Abrir Completo</a></td>
        </tr>""" for d in dados])

        conteudo = f"""
        <h4>🦷 Prontuários Odontológicos</h4>
        <form method="GET" class="row mb-3">
            <input type="hidden" name="consultar" value="1">
            <div class="col-md-10"><input type="text" name="busca" value="{busca}" class="form-control" placeholder="Buscar por paciente..."></div>
            <div class="col-md-2"><button class="btn btn-primary w-100">Buscar</button></div>
        </form>
        <a href="/dentista/prontuario/" class="btn btn-secondary mb-3">Voltar</a>
        <div style="overflow-x:auto;">
            <table class="table table-bordered table-hover">
                <thead class="table-dark"><tr><th>Paciente</th><th>Data</th><th>Dente</th><th>Queixa</th><th>Diagnóstico</th><th>Procedimento</th><th>Ação</th></tr></thead>
                <tbody>{linhas or '<tr><td colspan="7" class="text-center">Sem registros</td></tr>'}</tbody>
            </table>
        </div>"""
        return render_page("Consulta Prontuários", conteudo)

    if not agendamento_id:
        return render_page("Erro", "ID do agendamento não informado.")

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.nome, p.telefone, c.nome, pr.id, pr.nome,
                   ag.data_agendamento, ag.horario_selecionado
            FROM agendamentos ag
            JOIN pacientes p ON ag.paciente_id = p.id
            LEFT JOIN convenios c ON p.convenio_id = c.id
            JOIN agendas_config ac ON ag.agenda_config_id = ac.id
            JOIN profissionais pr ON ac.profissional_id = pr.id
            WHERE ag.id = %s
        """, [agendamento_id])
        dados = cursor.fetchone()
        if not dados:
            return render_page("Erro", "Agendamento não encontrado.")
        pac_id, pac_nome_bruto, pac_tel, conv_nome, prof_id, prof_nome, data, hora = dados
        pac_nome = pac_nome_bruto.split("(Ag:")[0].strip() if "(Ag:" in pac_nome_bruto else pac_nome_bruto

    if request.method == "POST":
        queixa = request.POST.get('queixa')
        diagnostico = request.POST.get('diagnostico')
        procedimento = request.POST.get('procedimento')
        dente = request.POST.get('dente')
        observacoes = request.POST.get('observacoes')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO prontuarios_odonto
                    (paciente_id, profissional_id, data_atendimento, hora,
                     queixa, diagnostico, procedimentos, dente, observacoes)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, [pac_id, prof_id, data, hora, queixa, diagnostico, procedimento, dente, observacoes])
                cursor.execute("UPDATE agendamentos SET status = 'Finalizado' WHERE id = %s", [agendamento_id])
            return HttpResponseRedirect('/dentista/prontuario/')
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT data_atendimento, diagnostico, procedimentos, queixa, dente
            FROM prontuarios_odonto
            WHERE paciente_id = %s AND profissional_id = %s
            ORDER BY data_atendimento DESC
        """, [pac_id, prof_id_logado])
        historico_lista = cursor.fetchall()

    lista_hist = "".join([f"""
        <div class='card mb-2 border-start border-primary border-4 shadow-sm'>
            <div class='card-body py-2'>
                <small class='fw-bold text-primary'>{h[0].strftime('%d/%m/%Y')}</small><br>
                <b>Dente:</b> {h[4] or '-'}<br>
                <b>Queixa:</b> {h[3]}<br><b>Diagnóstico:</b> {h[1]}
            </div>
        </div>""" for h in historico_lista])

    conteudo = f"""
    <div class="container-fluid py-2">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4>🦷 Atendimento Odontológico</h4>
            <div>
                <a href="?consultar=1" class="btn btn-info btn-sm me-2">📋 Consultar Prontuários</a>
                <a href="/dentista/prontuario/" class="btn btn-outline-secondary btn-sm">Sair sem salvar</a>
            </div>
        </div>
        {mensagem}
        <div class="row">
            <div class="col-md-8">
                <div class="card p-3 mb-3"><b>Paciente:</b> {pac_nome}<br><b>Convênio:</b> {conv_nome or 'Particular'}</div>
                <form method="POST" class="row g-3">
                    <div class="col-md-6">
                        <label class="fw-bold">Dente(s)</label>
                        <input type="text" name="dente" class="form-control" placeholder="Ex: 11, 12, 36...">
                    </div>
                    <div class="col-md-6">
                        <label class="fw-bold">Procedimento Realizado</label>
                        <input type="text" name="procedimento" class="form-control" placeholder="Ex: Extração, Restauração...">
                    </div>
                    <div class="col-12">
                        <label class="fw-bold">Queixa Principal</label>
                        <textarea name="queixa" class="form-control mb-2" rows="3" required></textarea>
                    </div>
                    <div class="col-12">
                        <label class="fw-bold">Diagnóstico</label>
                        <textarea name="diagnostico" class="form-control mb-2" rows="3"></textarea>
                    </div>
                    <div class="col-12">
                        <label class="fw-bold">Observações</label>
                        <textarea name="observacoes" class="form-control mb-3" rows="2"></textarea>
                    </div>
                    <div class="col-12">
                        <button class="btn btn-primary w-100 fw-bold">Salvar Prontuário Odontológico</button>
                    </div>
                </form>
            </div>
            <div class="col-md-4">
                <h6 class="fw-bold">Histórico do Paciente</h6>
                {lista_hist or '<p class="text-muted">Sem histórico</p>'}
            </div>
        </div>
    </div>"""
    return render_page("Prontuário Odontológico", conteudo)


# --- ACESSOS ---
@login_required
@csrf_exempt
def acesso_geral(request):
    User = get_user_model()
    if request.method == "POST":
        nome = request.POST.get('nome')
        user = request.POST.get('username')
        senha = request.POST.get('senha')
        cargo = request.POST.get('cargo')
        if not User.objects.filter(username=user).exists():
            u_obj = User.objects.create_user(username=user, password=senha)
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO perfis_usuario (user_id, nome_completo, cargo) VALUES (%s,%s,%s)",
                    [u_obj.id, nome, cargo]
                )
        return HttpResponseRedirect('/acessos/')

    return HttpResponse(base_html("Acessos", """
        <h4>Cadastro de Usuários</h4>
        <form method='POST' class='row g-3' style='max-width:400px;'>
            <div class='col-12'><label>Nome Completo</label><input name='nome' class='form-control' required></div>
            <div class='col-12'><label>Login</label><input name='username' class='form-control' required></div>
            <div class='col-12'><label>Senha</label><input name='senha' type='password' class='form-control' required></div>
            <div class='col-12'>
                <label>Cargo</label>
                <select name='cargo' class='form-select'>
                    <option>Administrador</option>
                    <option>Recepção</option>
                    <option>Médico</option>
                    <option>Dentista</option>
                </select>
            </div>
            <div class='col-12'><button class='btn btn-dark w-100'>Criar Usuário</button></div>
        </form>
    """))
