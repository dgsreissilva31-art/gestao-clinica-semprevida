from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- 1. TEMPLATE BASE (O "MOLDE" DO SISTEMA) ---
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
            .navbar-top {{ background-color: var(--top-bg); height: 50px; position: fixed; width: 100%; top: 0; z-index: 1000; color: white; display: flex; align-items: center; padding: 0 15px; }}
            .sidebar {{ background-color: var(--sidebar-bg); width: var(--sidebar-width); height: 100vh; position: fixed; top: 0; left: 0; padding-top: 50px; z-index: 999; }}
            .sidebar-header {{ padding: 15px; color: white; background: #1a2226; font-size: 14px; display: flex; align-items: center; gap: 10px; }}
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
            <div><i class="bi bi-list fs-4" style="cursor:pointer" onclick="document.querySelector('.sidebar').classList.toggle('active')"></i> <span class="ms-2 fw-bold text-uppercase">milestone</span></div>
            <div><i class="bi bi-person-circle"></i> Douglas Silva</div>
        </div>
        <div class="sidebar">
            <div class="sidebar-header">
                <i class="bi bi-person-circle fs-3"></i>
                <div><b>Douglas Silva</b><br><small><i class="bi bi-circle-fill text-success" style="font-size: 8px;"></i> Online</small></div>
            </div>
            <ul class="sidebar-menu">
                <div class="menu-label">Navegação</div>
                <li><a href="/"><i class="bi bi-speedometer2"></i> Dashboard</a></li>
                <div class="menu-label">Administrativo</div>
                <li><a href="/unidades/"><i class="bi bi-building"></i> Unidades</a></li>
                <li><a href="/especialidades/"><i class="bi bi-hospital"></i> Especialidades</a></li>
                <li><a href="/profissionais/"><i class="bi bi-person-badge"></i> Profissionais</a></li>
                <div class="menu-label">Operacional</div>
                <li><a href="#"><i class="bi bi-calendar-event"></i> Agendamentos</a></li>
                <li><a href="#"><i class="bi bi-cash-stack"></i> Financeiro</a></li>
            </ul>
        </div>
        <div class="main-content">
            <div class="card-panel">{conteudo}</div>
        </div>
    </body>
    </html>
    """

# --- 2. TELA 0: PAINEL DE GESTÃO ---
def painel_controle(request):
    conteudo = """
        <div class="mb-4">
            <h3 class="fw-bold"><i class="bi bi-speedometer2"></i> Painel de Gestão</h3>
            <p class="text-muted">Bem-vindo ao sistema Sempre Vida.</p>
        </div>
        <div class="row g-3">
            <div class="col-md-4">
                <div class="p-4 bg-primary text-white rounded shadow-sm text-center">
                    <i class="bi bi-building fs-1"></i><br><h5 class="mt-2">Unidades</h5>
                    <a href="/unidades/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-success text-white rounded shadow-sm text-center">
                    <i class="bi bi-hospital fs-1"></i><br><h5 class="mt-2">Especialidades</h5>
                    <a href="/especialidades/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-warning text-dark rounded shadow-sm text-center border">
                    <i class="bi bi-person-badge fs-1"></i><br><h5 class="mt-2">Profissionais</h5>
                    <a href="/profissionais/" class="btn btn-sm btn-dark mt-2 text-white fw-bold">Acessar</a>
                </div>
            </div>
        <div class="col-md-4">
    <div class="p-4 bg-info text-white rounded shadow-sm text-center">
        <i class="bi bi-card-checklist fs-1"></i><br><h5 class="mt-2">Convênios</h5>
        <a href="/convenios/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a>
    </div>
  </div>
</div>
        
    """
    return HttpResponse(base_html("Dashboard", conteudo))

# --- 3. TELA 1: UNIDADES ---
@csrf_exempt
def cadastro_unidade(request):
    mensagem = ""
    if request.method == "POST":
        nome, end, tel = request.POST.get('nome'), request.POST.get('endereco'), request.POST.get('telefone')
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO unidades (nome, endereco, telefone) VALUES (%s, %s, %s)", [nome, end, tel])
            mensagem = '<div class="alert alert-success">✅ Unidade Salva!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'
    
    conteudo = f"""
        <h4><i class="bi bi-plus-circle"></i> Nova Unidade</h4><hr>
        {mensagem}
        <form method="POST" class="row g-3">
            <div class="col-md-6"><label class="form-label">Nome</label><input type="text" name="nome" class="form-control" required></div>
            <div class="col-md-6"><label class="form-label">Telefone</label><input type="text" name="telefone" class="form-control"></div>
            <div class="col-12"><label class="form-label">Endereço</label><input type="text" name="endereco" class="form-control"></div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">Salvar</button>
                <a href="/unidades/lista/" class="btn btn-outline-dark">Listar Unidades</a>
            </div>
        </form>
    """
    return HttpResponse(base_html("Nova Unidade", conteudo))

def lista_unidades(request):
    if request.GET.get('delete'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM unidades WHERE id = %s", [request.GET.get('delete')])
        return HttpResponseRedirect('/unidades/lista/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, endereco FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()
    linhas = "".join([f'<tr><td>{u[1]}</td><td>{u[2]}</td><td><a href="/unidades/lista/?delete={u[0]}" class="btn btn-sm btn-danger" onclick="return confirm(\'Deseja excluir?\')"><i class="bi bi-trash"></i></a></td></tr>' for u in unidades])
    conteudo = f"<h4>Unidades Ativas</h4><hr><table class='table table-hover'><thead class='table-light'><tr><th>Nome</th><th>Endereço</th><th>Ação</th></tr></thead><tbody>{linhas}</tbody></table><a href='/unidades/' class='btn btn-primary'>Voltar</a>"
    return HttpResponse(base_html("Lista Unidades", conteudo))

# --- 4. TELA 2: ESPECIALIDADES ---
@csrf_exempt
def especialidades_geral(request):
    if request.GET.get('delete_esp'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM especialidades WHERE id = %s", [request.GET.get('delete_esp')])
        return HttpResponseRedirect('/especialidades/')
    if request.method == "POST":
        nome, tipo = request.POST.get('nome'), request.POST.get('tipo')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO especialidades (nome, tipo) VALUES (%s, %s)", [nome, tipo])
        return HttpResponseRedirect('/especialidades/')
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, tipo FROM especialidades ORDER BY tipo, nome")
        dados = cursor.fetchall()
    itens = "".join([f'<tr><td>{d[1]}</td><td>{d[2]}</td><td><a href="/especialidades/?delete_esp={d[0]}" class="btn btn-sm btn-danger" onclick="return confirm(\'Deseja excluir?\')"><i class="bi bi-trash"></i></a></td></tr>' for d in dados])
    conteudo = f"<h4>Especialidades</h4><hr><form method='POST' class='row g-2 mb-4'><div class='col-md-6'><input type='text' name='nome' class='form-control' placeholder='Especialidade' required></div><div class='col-md-4'><select name='tipo' class='form-select'><option value='Médica'>Médica</option><option value='Odontológica'>Odontológica</option></select></div><div class='col-md-2'><button type='submit' class='btn btn-primary w-100'>Salvar</button></div></form><table class='table table-sm table-hover'><thead><tr><th>Nome</th><th>Tipo</th><th>Ação</th></tr></thead><tbody>{itens}</tbody></table>"
    return HttpResponse(base_html("Especialidades", conteudo))


# --- 5. TELA 3: PROFISSIONAIS (ATUALIZADA COM TELEFONE E ENDEREÇO) ---
@csrf_exempt
def profissionais_geral(request):
    if request.GET.get('delete_prof'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM profissionais WHERE id = %s", [request.GET.get('delete_prof')])
        return HttpResponseRedirect('/profissionais/')

    if request.method == "POST":
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        num = request.POST.get('numero')
        esp = request.POST.get('especialidade_id')
        tel = request.POST.get('telefone')
        end = request.POST.get('endereco')
        
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO profissionais (nome, conselho_tipo, conselho_numero, especialidade_id, telefone, endereco) VALUES (%s, %s, %s, %s, %s, %s)", 
                [nome, tipo, num, esp, tel, end]
            )
        return HttpResponseRedirect('/profissionais/')

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM especialidades ORDER BY nome")
        especialidades = cursor.fetchall()
        
        # Busca profissionais incluindo os novos campos
        cursor.execute("""
            SELECT p.id, p.nome, p.conselho_tipo, p.conselho_numero, e.nome, p.telefone, p.endereco 
            FROM profissionais p 
            LEFT JOIN especialidades e ON p.especialidade_id = e.id 
            ORDER BY p.nome
        """)
        profs = cursor.fetchall()

    opcoes = "".join([f'<option value="{e[0]}">{e[1]}</option>' for e in especialidades])
    
    linhas = "".join([f"""
        <tr>
            <td>{p[1]}<br><small class='text-muted'>📍 {p[6] if p[6] else '---'}</small></td>
            <td>{p[2]}: {p[3]}</td>
            <td>{p[4] if p[4] else "---"}</td>
            <td>{p[5] if p[5] else "---"}</td>
            <td><a href="/profissionais/?delete_prof={p[0]}" class="btn btn-sm btn-danger" onclick="return confirm('Deseja excluir?')"><i class="bi bi-trash"></i></a></td>
        </tr>""" for p in profs])

    conteudo = f"""
        <h4><i class="bi bi-person-badge"></i> Cadastro de Profissionais</h4><hr>
        <form method='POST' class='row g-3 mb-4'>
            <div class='col-md-4'><label class='form-label fw-bold'>Nome Completo</label><input type='text' name='nome' class='form-control' required></div>
            <div class='col-md-2'><label class='form-label fw-bold'>Conselho</label><select name='tipo' class='form-select'><option value='CRM'>CRM</option><option value='CRO'>CRO</option></select></div>
            <div class='col-md-2'><label class='form-label fw-bold'>Número</label><input type='text' name='numero' class='form-control' required></div>
            <div class='col-md-4'><label class='form-label fw-bold'>Especialidade</label><select name='especialidade_id' class='form-select'>{opcoes}</select></div>
            
            <div class='col-md-4'><label class='form-label fw-bold'>Telefone</label><input type='text' name='telefone' class='form-control' placeholder='(00) 00000-0000'></div>
            <div class='col-md-8'><label class='form-label fw-bold'>Endereço Completo</label><input type='text' name='endereco' class='form-control' placeholder='Rua, número, bairro...'></div>
            
            <div class='col-12'><button type='submit' class='btn btn-warning w-100 fw-bold'>Salvar Profissional</button></div>
        </form>
        <hr>
        <div class='table-responsive'>
            <table class='table table-hover'>
                <thead class='table-dark'><tr><th>Nome / Endereço</th><th>Registro</th><th>Especialidade</th><th>Telefone</th><th>Ação</th></tr></thead>
                <tbody>{linhas if profs else '<tr><td colspan="5" class="text-center">Nenhum cadastrado.</td></tr>'}</tbody>
            </table>
        </div>
    """
    return HttpResponse(base_html("Profissionais", conteudo))


# --- 7. TELA 4: GESTÃO DE CONVÊNIOS ---
@csrf_exempt
def convenios_geral(request):
    mensagem = ""
    # Lógica de Exclusão com Confirmação
    if request.GET.get('delete_conv'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM convenios WHERE id = %s", [request.GET.get('delete_conv')])
        return HttpResponseRedirect('/convenios/')

    # Lógica de Cadastro
    if request.method == "POST":
        nome = request.POST.get('nome')
        ans = request.POST.get('ans')
        tel = request.POST.get('telefone')
        end = request.POST.get('endereco')
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO convenios (nome, registro_ans, telefone_contato, endereco_completo) VALUES (%s, %s, %s, %s)",
                    [nome, ans, tel, end]
                )
            mensagem = '<div class="alert alert-success">✅ Convênio cadastrado com sucesso!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    # Busca Lista
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, registro_ans, telefone_contato, endereco_completo FROM convenios ORDER BY nome")
        conves = cursor.fetchall()

    linhas = "".join([f"""
        <tr>
            <td><b>{c[1]}</b><br><small class='text-muted'>📍 {c[4] if c[4] else '---'}</small></td>
            <td>{c[2] if c[2] else '---'}</td>
            <td>{c[3] if c[3] else '---'}</td>
            <td><a href="/convenios/?delete_conv={c[0]}" class="btn btn-sm btn-danger" onclick="return confirm('Deseja excluir este convênio?')"><i class="bi bi-trash"></i></a></td>
        </tr>""" for c in conves])

    conteudo = f"""
        <h4><i class="bi bi-card-checklist"></i> Cadastro de Convênios</h4><hr>
        {mensagem}
        <form method="POST" class="row g-3 mb-4">
            <div class="col-md-5"><label class="form-label fw-bold">Nome do Convênio</label><input type="text" name="nome" class="form-control" placeholder="Ex: Unimed, Bradesco..." required></div>
            <div class="col-md-3"><label class="form-label fw-bold">Registro ANS</label><input type="text" name="ans" class="form-control" placeholder="Cód. ANS"></div>
            <div class="col-md-4"><label class="form-label fw-bold">Telefone Suporte</label><input type="text" name="telefone" class="form-control" placeholder="(00) 0000-0000"></div>
            <div class="col-12"><label class="form-label fw-bold">Endereço da Operadora</label><input type="text" name="endereco" class="form-control" placeholder="Rua, número, cidade..."></div>
            <div class="col-12"><button type="submit" class="btn btn-info w-100 fw-bold text-white shadow-sm">Salvar Convênio</button></div>
        </form>
        <hr>
        <h5>Convênios Ativos</h5>
        <div class="table-responsive">
            <table class="table table-hover mt-2">
                <thead class="table-dark"><tr><th>Nome / Endereço</th><th>ANS</th><th>Contato</th><th>Ação</th></tr></thead>
                <tbody>{linhas if conves else '<tr><td colspan="4" class="text-center text-muted">Nenhum convênio cadastrado.</td></tr>'}</tbody>
            </table>
        </div>
        <a href="/" class="btn btn-outline-secondary mt-3">⬅️ Voltar ao Painel</a>
    """
    return HttpResponse(base_html("Convênios", conteudo))





# --- 6. ROTAS ---
urlpatterns = [
    path('', painel_controle),
    path('unidades/', cadastro_unidade),
    path('unidades/lista/', lista_unidades),
    path('especialidades/', especialidades_geral),
    path('profissionais/', profissionais_geral),
]


# --- ESSA PARTE FICA NO FINAL DE TUDO NO URLS.PY ---
urlpatterns = [
    path('', painel_controle),              # Painel Geral
    path('unidades/', cadastro_unidade),    # Cadastro Unidades
    path('unidades/lista/', lista_unidades), # Lista Unidades
    path('especialidades/', especialidades_geral), # Especialidades
    path('profissionais/', profissionais_geral),   # Médicos/Dentistas
    path('convenios/', convenios_geral),           # <--- A NOVA TELA AQUI
]
