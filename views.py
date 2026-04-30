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


# --- PAINEL DE CONTROLE ---
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


# --- UNIDADES ---
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
@cargo_required('Administrador')
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


# --- RECEPÇÃO ---
@login_required
@csrf_exempt
def recepcao_geral(request):
    data_hoje = datetime.date.today()
    mensagem = ""
    usuario_nome = request.user.username if request.user.is_authenticated else "sistema"

    unidade_filtro = request.POST.get('unidade_id_hidden') or request.GET.get('unidade') or ""
    profissional_filtro = request.GET.get('profissional') or ""
    agendamento_id = request.GET.get('fluxo_id')
    etapa = request.GET.get('etapa', '1')

    # Busca cargo do usuário logado
    with connection.cursor() as cursor:
        cursor.execute("SELECT cargo FROM perfis_usuario WHERE user_id = %s", [request.user.id])
        cargo_res = cursor.fetchone()
    cargo_atual = cargo_res[0] if cargo_res else ""

    if request.method == "POST" and "finalizar_fluxo" in request.POST:
        try:
            ag_id = request.POST.get('ag_id')
            tipo = request.POST.get('tipo_pagto')
            convenio_id = request.POST.get('convenio_id')
            retorno = request.POST.get('retorno')

            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT pac.nome, prof.nome, u.id
                    FROM agendamentos ag
                    JOIN pacientes pac ON ag.paciente_id = pac.id
                    JOIN agendas_config ac ON ag.agenda_config_id = ac.id
                    JOIN profissionais prof ON ac.profissional_id = prof.id
                    JOIN unidades u ON ac.unidade_id = u.id
                    WHERE ag.id = %s
                """, [ag_id])
                info = cursor.fetchone()
                if not info:
                    raise Exception("Agendamento não encontrado")

                paciente_nome, profissional_nome, unidade_id = info
                descricao_base = "Retorno" if retorno else "Particular"

                if tipo == "avista":
                    valor = float(request.POST.get('valor') or 0)
                    if valor <= 0: raise Exception("Informe o valor")
                    forma = request.POST.get('forma_pagamento') or "Pix"
                    cursor.execute("""
                        INSERT INTO caixa (paciente_nome, profissional_nome, valor, forma_pagamento, status,
                         categoria, descricao, data_pagamento, unidade_id, usuario_lancamento)
                        VALUES (%s,%s,%s,%s,'Pago','Consulta',%s,CURRENT_DATE,%s,%s)
                    """, [paciente_nome, profissional_nome, valor, forma, descricao_base, unidade_id, usuario_nome])

                elif tipo == "convenio":
                    convenio_nome = ""
                    if convenio_id:
                        cursor.execute("SELECT nome FROM convenios WHERE id = %s", [convenio_id])
                        c = cursor.fetchone()
                        if c: convenio_nome = c[0]
                    cursor.execute("""
                        INSERT INTO caixa (paciente_nome, profissional_nome, valor, forma_pagamento, status,
                         categoria, descricao, data_pagamento, unidade_id, usuario_lancamento)
                        VALUES (%s,%s,0,'Faturado','A Faturar','Consulta',%s,CURRENT_DATE,%s,%s)
                    """, [paciente_nome, profissional_nome, "Retorno" if retorno else (convenio_nome or "Convênio"), unidade_id, usuario_nome])

                elif tipo == "cartao":
                    valor = float(request.POST.get('valor') or 0)
                    if valor <= 0: raise Exception("Informe o valor")
                    forma = request.POST.get('forma_pagamento') or "Pix"
                    convenio_nome = ""
                    if convenio_id:
                        cursor.execute("SELECT nome FROM convenios WHERE id = %s", [convenio_id])
                        c = cursor.fetchone()
                        if c: convenio_nome = c[0]
                    cursor.execute("""
                        INSERT INTO caixa (paciente_nome, profissional_nome, valor, forma_pagamento, status,
                         categoria, descricao, data_pagamento, unidade_id, usuario_lancamento)
                        VALUES (%s,%s,%s,%s,'Pago','Consulta',%s,CURRENT_DATE,%s,%s)
                    """, [paciente_nome, profissional_nome, valor, forma,
                          f"Cartão: {convenio_nome}" if convenio_nome else "Cartão Desconto",
                          unidade_id, usuario_nome])

                cursor.execute("UPDATE agendamentos SET status = 'Chegada' WHERE id = %s", [ag_id])

            return redirect(f"/recepcao/?unidade={unidade_filtro}&profissional={profissional_filtro}")

        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ {e}</div>'

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades_lista = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM convenios ORDER BY nome")
        convenios_lista = cursor.fetchall()
        if unidade_filtro:
            cursor.execute("""
                SELECT DISTINCT prof.id, prof.nome
                FROM profissionais prof
                JOIN agendas_config ac ON ac.profissional_id = prof.id
                WHERE ac.unidade_id = %s ORDER BY prof.nome
            """, [unidade_filtro])
        else:
            cursor.execute("SELECT id, nome FROM profissionais ORDER BY nome")
        profissionais_lista = cursor.fetchall()

        sql = """
            SELECT ag.id, pac.nome, prof.nome, ag.horario_selecionado, ag.status
            FROM agendamentos ag
            LEFT JOIN pacientes pac ON ag.paciente_id = pac.id
            LEFT JOIN agendas_config ac ON ag.agenda_config_id = ac.id
            LEFT JOIN profissionais prof ON ac.profissional_id = prof.id
            LEFT JOIN unidades u ON ac.unidade_id = u.id
            WHERE ag.data_agendamento = %s
        """
        params = [data_hoje]
        if unidade_filtro:
            sql += " AND u.id = %s"; params.append(unidade_filtro)
        if profissional_filtro:
            sql += " AND prof.id = %s"; params.append(profissional_filtro)
        sql += " ORDER BY ag.horario_selecionado"
        cursor.execute(sql, params)
        agenda = cursor.fetchall()

    opts_unidades = "".join([f'<option value="{u[0]}" {"selected" if str(unidade_filtro)==str(u[0]) else ""}>{u[1]}</option>' for u in unidades_lista])
    opts_conv = "".join([f'<option value="{c[0]}">{c[1]}</option>' for c in convenios_lista])
    opts_prof = "".join([f'<option value="{p[0]}" {"selected" if str(profissional_filtro)==str(p[0]) else ""}>{p[1]}</option>' for p in profissionais_lista])

    linhas = ""
    for a in agenda:
        status = a[4] or "Agendado"
        if status == "Agendado":
            btn_acao = f'<a href="?fluxo_id={a[0]}&etapa=2&unidade={unidade_filtro}&profissional={profissional_filtro}" class="btn btn-warning btn-sm">Check-in</a>'
        elif status == "Chegada":
            btn_prontuario = f'<a href="/prontuario/?id={a[0]}" class="btn btn-success btn-sm">Prontuário</a>'
            btn_refazer = ""
            if cargo_atual != "Médico":
                btn_refazer = f' <a href="?fluxo_id={a[0]}&etapa=2&unidade={unidade_filtro}&profissional={profissional_filtro}" class="btn btn-outline-danger btn-sm">Alterar Check-in</a>'
            btn_acao = btn_prontuario + btn_refazer
        else:
            btn_acao = f'<span class="badge bg-secondary">{status}</span>'
        linhas += f"<tr><td>{str(a[3])[:5]}</td><td>{a[1]}</td><td>{a[2]}</td><td>{btn_acao}</td></tr>"

    modal_html = ""
    if agendamento_id and etapa == '2':
        modal_html = f"""
        <div class="modal fade show d-block" style="background:rgba(0,0,0,0.6)">
            <div class="modal-dialog">
                <div class="modal-content p-4">
                    <form method="POST">
                        <input type="hidden" name="ag_id" value="{agendamento_id}">
                        <input type="hidden" name="unidade_id_hidden" value="{unidade_filtro}">
                        <h5>Financeiro</h5>
                        <select name="tipo_pagto" id="tipo" class="form-select mb-2" onchange="toggle()">
                            <option value="avista">Particular</option>
                            <option value="convenio">Convênio</option>
                            <option value="cartao">Cartão Desconto</option>
                        </select>
                        <select name="convenio_id" id="convenio" class="form-select mb-2">
                            <option value="">Selecione Convênio</option>
                            {opts_conv}
                        </select>
                        <div class="mb-2" id="div_retorno" style="display:none;">
                            <input type="checkbox" name="retorno" value="1"> Retorno
                        </div>
                        <div id="pagamento">
                            <input type="number" step="0.01" name="valor" class="form-control mb-2" placeholder="Valor">
                            <select name="forma_pagamento" class="form-select mb-3">
                                <option>Pix</option><option>Cartão</option><option>Dinheiro</option>
                            </select>
                        </div>
                        <button name="finalizar_fluxo" class="btn btn-success w-100">FINALIZAR</button>
                        <a href="/recepcao/?unidade={unidade_filtro}&profissional={profissional_filtro}"
                           class="btn btn-outline-secondary w-100 mt-2">Cancelar</a>
                    </form>
                </div>
            </div>
        </div>
        <script>
        function toggle() {{
            var tipo = document.getElementById("tipo").value;
            var pag = document.getElementById("pagamento");
            var conv = document.getElementById("convenio");
            var ret = document.getElementById("div_retorno");
            if (tipo === "convenio") {{ pag.style.display="none"; conv.style.display="block"; ret.style.display="block"; }}
            else if (tipo === "cartao") {{ pag.style.display="block"; conv.style.display="block"; ret.style.display="none"; }}
            else {{ pag.style.display="block"; conv.style.display="none"; ret.style.display="none"; }}
        }}
        toggle();
        </script>
        """

    conteudo = f"""
    <h4>Recepção</h4>
    <form method="GET" class="row g-2 mb-3">
        <div class="col-md-6">
            <select name="unidade" class="form-select" onchange="this.form.submit()">
                <option value="">Todas as Unidades</option>{opts_unidades}
            </select>
        </div>
        <div class="col-md-6">
            <select name="profissional" class="form-select" onchange="this.form.submit()">
                <option value="">Todos os Profissionais</option>{opts_prof}
            </select>
        </div>
    </form>
    {mensagem}
    <table class="table table-hover">
        <thead class="table-light"><tr><th>Hora</th><th>Paciente</th><th>Médico</th><th>Ação</th></tr></thead>
        <tbody>{linhas}</tbody>
    </table>
    {modal_html}
    """
    return HttpResponse(base_html("Recepção", conteudo))


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
            body {{ background: #f0f4f8; font-family: 'Segoe UI', sans-serif; }}
            .topbar {{ background: linear-gradient(135deg,#1a6b3c,#27ae60); color:white; padding:12px 24px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 6px rgba(0,0,0,0.2); position:fixed; width:100%; top:0; z-index:1000; }}
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
            <div style="font-size:18px; font-weight:bold;"><i class="bi bi-heart-pulse-fill"></i> &nbsp;SEMPRE VIDA</div>
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
            body {{ background: #f0f4f8; font-family: 'Segoe UI', sans-serif; }}
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
            <div style="font-size:18px; font-weight:bold;"><i class="bi bi-mask"></i> &nbsp;SEMPRE VIDA</div>
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
