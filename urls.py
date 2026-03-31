import datetime
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

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
            <div><i class="bi bi-list fs-4" style="cursor:pointer" onclick="document.querySelector('.sidebar').classList.toggle('active')"></i> <span class="ms-2 fw-bold text-uppercase">milestone</span></div>
            <div><i class="bi bi-person-circle"></i> Douglas Silva</div>
        </div>
        <div class="sidebar">
            <ul class="sidebar-menu">
                <div class="menu-label">Navegação</div>
                <li><a href="/"><i class="bi bi-speedometer2"></i> Dashboard</a></li>
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
                <li><a href="/agenda-diaria/"><i class="bi bi-calendar3"></i> Agenda do Dia</a></li>
                <li><a href="/agendar/"><i class="bi bi-calendar-plus"></i> Novo Agendamento</a></li>
              
               
                
                
                
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
            <div class="col-md-4">
                <div class="p-4 bg-secondary text-white rounded shadow-sm text-center">
                    <i class="bi bi-microscope fs-1"></i><br><h5 class="mt-2">Exames</h5>
                    <a href="/exames/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a>
                </div>
            </div>
            <div class="col-md-4">
    <div class="p-4 bg-dark text-white rounded shadow-sm text-center">
        <i class="bi bi-mask fs-1"></i><br><h5 class="mt-2">Odontologia</h5>
        <a href="/odontologia/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a>
      </div>
    </div>
    <div class="col-md-4">
    <div class="p-4 bg-danger text-white rounded shadow-sm text-center">
        <i class="bi bi-people fs-1"></i><br><h5 class="mt-2">Pacientes</h5>
        <a href="/pacientes/" class="btn btn-sm btn-light mt-2 fw-bold">Acessar</a>
    </div>
  </div>
  <div class="col-md-4">
    <div class="p-4 bg-dark text-white rounded shadow-sm text-center">
        <i class="bi bi-shield-lock fs-1"></i><br><h5 class="mt-2">Acessos</h5>
        <a href="/acessos/" class="btn btn-sm btn-light mt-2 fw-bold">Configurar</a>
    </div>
  </div>
  <div class="col-md-4">
    <div class="p-4 bg-primary text-white rounded shadow-sm text-center">
        <i class="bi bi-currency-dollar fs-1"></i><br><h5 class="mt-2">Tabela de Preços</h5>
        <a href="/precos/" class="btn btn-sm btn-light mt-2 fw-bold">Configurar</a>
    </div>
  </div>
  <div class="col-md-4">
    <div class="p-4 bg-info text-white rounded shadow-sm text-center">
        <i class="bi bi-tags fs-1"></i><br><h5 class="mt-2">Preços Exames</h5>
        <a href="/precos-exames/" class="btn btn-sm btn-light mt-2 fw-bold">Configurar</a>
    </div>
  </div>
  <div class="col-md-4">
    <div class="p-4 bg-success text-white rounded shadow-sm text-center">
        <i class="bi bi-calendar-check fs-1"></i><br><h5 class="mt-2">Configurar Agendas</h5>
        <a href="/agendas-config/" class="btn btn-sm btn-light mt-2 fw-bold">Configurar</a>
    </div>
  </div>
  <div class="col-md-4">
    <div class="p-4 bg-light text-dark rounded shadow-sm text-center border">
        <i class="bi bi-calendar3 fs-1 text-primary"></i><br><h5 class="mt-2 text-primary">Agenda do Dia</h5>
        <a href="/agenda-diaria/" class="btn btn-sm btn-primary mt-2 fw-bold text-white">Ver Calendário</a>
    </div>
</div>
    <div class="col-md-4 mb-3">
    <div class="card text-center shadow-sm">
        <div class="card-body">
            <i class="bi bi-calendar-check-fill text-success fs-1"></i>
            <h5 class="card-title mt-2">Novo Agendamento</h5>
            <p class="small text-muted">Marcar consulta manualmente</p>
            <a href="/agendar/" class="btn btn-success btn-sm w-100">Abrir Tela 13</a>
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




# --- 8. TELA 5: GESTÃO DE EXAMES (ATUALIZADA COM GRUPO) ---
@csrf_exempt
def exames_geral(request):
    mensagem = ""
    # Exclusão
    if request.GET.get('delete_exame'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM exames WHERE id = %s", [request.GET.get('delete_exame')])
        return HttpResponseRedirect('/exames/')

    # Cadastro
    if request.method == "POST":
        nome = request.POST.get('nome')
        grupo = request.POST.get('grupo')
        preparo = request.POST.get('preparo')
        valor = request.POST.get('valor')
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO exames (nome, grupo, preparo, valor_particular) VALUES (%s, %s, %s, %s)",
                    [nome, grupo, preparo, valor if valor else 0]
                )
            mensagem = '<div class="alert alert-success">✅ Exame cadastrado com sucesso!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    # Busca Lista
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, preparo, valor_particular, grupo FROM exames ORDER BY grupo, nome")
        exames_lista = cursor.fetchall()

    linhas = "".join([f"""
        <tr>
            <td><b>{ex[1]}</b><br><span class="badge bg-light text-dark border">{ex[4] if ex[4] else 'Geral'}</span></td>
            <td><small>{ex[2] if ex[2] else 'Sem preparo específico.'}</small></td>
            <td>R$ {ex[3]}</td>
            <td><a href="/exames/?delete_exame={ex[0]}" class="btn btn-sm btn-danger" onclick="return confirm('Excluir este exame?')"><i class="bi bi-trash"></i></a></td>
        </tr>""" for ex in exames_lista])

    conteudo = f"""
        <h4><i class="bi bi-microscope"></i> Cadastro de Exames</h4><hr>
        {mensagem}
        <form method="POST" class="row g-3 mb-4">
            <div class="col-md-5"><label class="form-label fw-bold">Nome do Exame</label><input type="text" name="nome" class="form-control" placeholder="Ex: Hemograma" required></div>
            <div class="col-md-4"><label class="form-label fw-bold">Grupo / Categoria</label><input type="text" name="grupo" class="form-control" placeholder="Ex: Sangue, Imagem..."></div>
            <div class="col-md-3"><label class="form-label fw-bold">Valor (R$)</label><input type="number" step="0.01" name="valor" class="form-control" placeholder="0.00"></div>
            <div class="col-12"><label class="form-label fw-bold">Instruções de Preparo</label><textarea name="preparo" class="form-control" rows="2" placeholder="Ex: Jejum de 8 horas..."></textarea></div>
            <div class="col-12"><button type="submit" class="btn btn-secondary w-100 fw-bold shadow-sm">Salvar Exame</button></div>
        </form>
        <hr>
        <h5>Lista de Exames</h5>
        <div class="table-responsive">
            <table class="table table-hover mt-2">
                <thead class="table-dark"><tr><th>Exame / Grupo</th><th>Preparo</th><th>Valor</th><th>Ação</th></tr></thead>
                <tbody>{linhas if exames_lista else '<tr><td colspan="4" class="text-center text-muted">Nenhum exame cadastrado.</td></tr>'}</tbody>
            </table>
        </div>
        <a href="/" class="btn btn-outline-secondary mt-3">⬅️ Voltar ao Painel</a>
    """
    return HttpResponse(base_html("Exames", conteudo))


# --- 9. TELA 6: GESTÃO DE ODONTOLOGIA ---
@csrf_exempt
def odonto_geral(request):
    mensagem = ""
    # Exclusão
    if request.GET.get('delete_odonto'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM odontologia WHERE id = %s", [request.GET.get('delete_odonto')])
        return HttpResponseRedirect('/odontologia/')

    # Cadastro
    if request.method == "POST":
        proc = request.POST.get('procedimento')
        grupo = request.POST.get('grupo')
        valor = request.POST.get('valor')
        obs = request.POST.get('observacoes')
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO odontologia (procedimento, grupo, valor_particular, observacoes) VALUES (%s, %s, %s, %s)",
                    [proc, grupo, valor if valor else 0, obs]
                )
            mensagem = '<div class="alert alert-success">✅ Procedimento odontológico salvo!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    # Busca Lista
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, procedimento, grupo, valor_particular, observacoes FROM odontologia ORDER BY grupo, procedimento")
        lista_odonto = cursor.fetchall()

    linhas = "".join([f"""
        <tr>
            <td><b>{o[1]}</b><br><span class="badge bg-light text-dark border">{o[2] if o[2] else 'Geral'}</span></td>
            <td>R$ {o[3]}</td>
            <td><small>{o[4] if o[4] else '---'}</small></td>
            <td><a href="/odontologia/?delete_odonto={o[0]}" class="btn btn-sm btn-danger" onclick="return confirm('Excluir este procedimento?')"><i class="bi bi-trash"></i></a></td>
        </tr>""" for o in lista_odonto])

    conteudo = f"""
        <h4><i class="bi bi-mask"></i> Procedimentos Odontológicos</h4><hr>
        {mensagem}
        <form method="POST" class="row g-3 mb-4">
            <div class="col-md-5"><label class="form-label fw-bold">Procedimento</label><input type="text" name="procedimento" class="form-control" placeholder="Ex: Extração de Siso" required></div>
            <div class="col-md-4"><label class="form-label fw-bold">Grupo</label><input type="text" name="grupo" class="form-control" placeholder="Ex: Cirurgia, Estética..."></div>
            <div class="col-md-3"><label class="form-label fw-bold">Valor (R$)</label><input type="number" step="0.01" name="valor" class="form-control" placeholder="0.00"></div>
            <div class="col-12"><label class="form-label fw-bold">Observações Técnicas</label><textarea name="observacoes" class="form-control" rows="2" placeholder="Notas sobre o procedimento..."></textarea></div>
            <div class="col-12"><button type="submit" class="btn btn-dark w-100 fw-bold shadow-sm" style="background-color: #555;">Salvar Procedimento</button></div>
        </form>
        <hr>
        <div class="table-responsive">
            <table class="table table-hover mt-2">
                <thead class="table-dark"><tr><th>Procedimento / Grupo</th><th>Valor</th><th>Obs.</th><th>Ação</th></tr></thead>
                <tbody>{linhas if lista_odonto else '<tr><td colspan="4" class="text-center text-muted">Nenhum procedimento cadastrado.</td></tr>'}</tbody>
            </table>
        </div>
        <a href="/" class="btn btn-outline-secondary mt-3">⬅️ Voltar ao Painel</a>
    """
    return HttpResponse(base_html("Odontologia", conteudo))


# --- 10. TELA 7: GESTÃO DE PACIENTES ---
@csrf_exempt
def pacientes_geral(request):
    mensagem = ""
    # Lógica de Exclusão
    if request.GET.get('delete_pac'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM pacientes WHERE id = %s", [request.GET.get('delete_pac')])
        return HttpResponseRedirect('/pacientes/')

    # Lógica de Cadastro (POST)
    if request.method == "POST":
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        sexo = request.POST.get('sexo')
        nasc = request.POST.get('data_nasc')
        tel = request.POST.get('telefone')
        conv = request.POST.get('convenio_id')
        cep = request.POST.get('cep')
        end = request.POST.get('endereco')
        cidade = request.POST.get('cidade')
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO pacientes (nome, cpf, sexo, data_nascimento, telefone, convenio_id, cep, endereco, cidade) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    [nome, cpf, sexo, nasc if nasc else None, tel, conv if conv else None, cep, end, cidade]
                )
            mensagem = '<div class="alert alert-success">✅ Paciente cadastrado com sucesso!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    # Busca Convênios para o Select e Lista de Pacientes para a Tabela
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM convenios ORDER BY nome")
        convenios = cursor.fetchall()
        
        cursor.execute("""
            SELECT p.id, p.nome, p.cpf, p.telefone, c.nome, p.sexo, p.cidade 
            FROM pacientes p 
            LEFT JOIN convenios c ON p.convenio_id = c.id 
            ORDER BY p.id DESC
        """)
        lista_pacientes = cursor.fetchall()

    opcoes_conv = "".join([f'<option value="{c[0]}">{c[1]}</option>' for c in convenios])
    
    linhas = "".join([f"""
        <tr>
            <td><b>{p[1]}</b><br><small class='text-muted'>{p[5]} | CPF: {p[2]}</small></td>
            <td>{p[3]}<br><small class='text-secondary'>{p[6] if p[6] else ''}</small></td>
            <td><span class="badge bg-info text-dark">{p[4] if p[4] else 'Particular'}</span></td>
            <td>
                <a href="/pacientes/?delete_pac={p[0]}" class="btn btn-sm btn-danger" 
                   onclick="return confirm('Tem certeza que deseja excluir este paciente?')">
                   <i class="bi bi-trash"></i>
                </a>
            </td>
        </tr>""" for p in lista_pacientes])

    conteudo = f"""
        <h4><i class="bi bi-people"></i> Cadastro de Pacientes</h4><hr>
        {mensagem}
        <form method="POST" class="row g-3 mb-4">
            <div class="col-md-5"><label class="form-label fw-bold">Nome Completo</label><input type="text" name="nome" class="form-control" required></div>
            <div class="col-md-3"><label class="form-label fw-bold">CPF</label><input type="text" name="cpf" class="form-control" placeholder="000.000.000-00"></div>
            <div class="col-md-2"><label class="form-label fw-bold">Sexo</label>
                <select name="sexo" class="form-select">
                    <option value="Masculino">Masculino</option>
                    <option value="Feminino">Feminino</option>
                    <option value="Outro">Outro</option>
                </select>
            </div>
            <div class="col-md-2"><label class="form-label fw-bold">Nascimento</label><input type="date" name="data_nasc" class="form-control"></div>
            
            <div class="col-md-4"><label class="form-label fw-bold">Telefone</label><input type="text" name="telefone" class="form-control" placeholder="(00) 00000-0000"></div>
            <div class="col-md-4"><label class="form-label fw-bold">Convênio</label><select name="convenio_id" class="form-select"><option value="">Particular</option>{opcoes_conv}</select></div>
            <div class="col-md-4"><label class="form-label fw-bold">CEP</label><input type="text" name="cep" class="form-control" placeholder="00000-000"></div>
            
            <div class="col-md-4"><label class="form-label fw-bold">Cidade</label><input type="text" name="cidade" class="form-control"></div>
            <div class="col-md-8"><label class="form-label fw-bold">Endereço Completo</label><input type="text" name="endereco" class="form-control" placeholder="Rua, número, bairro..."></div>
            
            <div class="col-12 mt-4">
                <button type="submit" class="btn btn-danger w-100 fw-bold shadow-sm">SALVAR PACIENTE</button>
            </div>
        </form>
        <hr>
        <h5>Pacientes Cadastrados</h5>
        <div class="table-responsive">
            <table class="table table-hover mt-2">
                <thead class="table-dark">
                    <tr><th>Paciente / Info</th><th>Contato / Cidade</th><th>Convênio</th><th>Ação</th></tr>
                </thead>
                <tbody>{linhas if lista_pacientes else '<tr><td colspan="4" class="text-center text-muted">Nenhum paciente encontrado.</td></tr>'}</tbody>
            </table>
        </div>
        <a href="/" class="btn btn-outline-secondary mt-3">⬅️ Voltar ao Painel</a>
    """
    return HttpResponse(base_html("Pacientes", conteudo))



from django.contrib.auth.models import User # Adicione este import no topo!

# --- 11. TELA 8: GESTÃO DE ACESSOS E FUNCIONÁRIOS ---
@csrf_exempt
def acesso_geral(request):
    mensagem = ""
    
    if request.method == "POST":
        nome = request.POST.get('nome')
        username = request.POST.get('username') # O login dele
        senha = request.POST.get('senha')
        cargo = request.POST.get('cargo')
        cpf = request.POST.get('cpf')

        try:
            # 1. Cria o usuário no sistema de login do Django
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=senha)
                
                # 2. Salva os detalhes extras na nossa tabela
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO perfis_usuario (user_id, nome_completo, cargo, cpf) VALUES (%s, %s, %s, %s)",
                        [user.id, nome, cargo, cpf]
                    )
                mensagem = f'<div class="alert alert-success">✅ Usuário {username} criado com sucesso!</div>'
            else:
                mensagem = '<div class="alert alert-danger">❌ Este login já existe!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    # Busca Lista de Funcionários
    with connection.cursor() as cursor:
        cursor.execute("SELECT nome_completo, cargo, cpf FROM perfis_usuario ORDER BY cargo, nome_completo")
        funcionarios = cursor.fetchall()

    linhas = "".join([f"<tr><td><b>{f[0]}</b></td><td>{f[1]}</td><td>{f[2]}</td></tr>" for f in funcionarios])

    conteudo = f"""
        <h4><i class="bi bi-shield-lock"></i> Controle de Acesso e Funcionários</h4><hr>
        {mensagem}
        <form method="POST" class="row g-3 mb-4">
            <div class="col-md-6"><label class="form-label fw-bold">Nome do Funcionário</label><input type="text" name="nome" class="form-control" required></div>
            <div class="col-md-3"><label class="form-label fw-bold">Cargo</label>
                <select name="cargo" class="form-select">
                    <option value="Recepção">Recepção</option>
                    <option value="Médico">Médico</option>
                    <option value="Dentista">Dentista</option>
                    <option value="Administrador">Administrador</option>
                </select>
            </div>
            <div class="col-md-3"><label class="form-label fw-bold">CPF</label><input type="text" name="cpf" class="form-control" placeholder="000.000.000-00"></div>
            
            <div class="col-md-6"><label class="form-label fw-bold">Login (Usuário)</label><input type="text" name="username" class="form-control" placeholder="Ex: douglas.silva" required></div>
            <div class="col-md-6"><label class="form-label fw-bold">Senha de Acesso</label><input type="password" name="senha" class="form-control" required></div>
            
            <div class="col-12"><button type="submit" class="btn btn-dark w-100 fw-bold shadow-sm">CRIAR ACESSO AO SISTEMA</button></div>
        </form>
        <hr>
        <div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-dark"><tr><th>Nome</th><th>Cargo</th><th>CPF</th></tr></thead>
                <tbody>{linhas if funcionarios else '<tr><td colspan="3" class="text-center">Nenhum funcionário cadastrado.</td></tr>'}</tbody>
            </table>
        </div>
        <a href="/" class="btn btn-outline-secondary mt-3">⬅️ Voltar ao Painel</a>
    """
    return HttpResponse(base_html("Acessos", conteudo))



# --- 12. TELA 9: PREÇOS DE CONSULTAS POR CONVÊNIO ---
@csrf_exempt
def precos_geral(request):
    mensagem = ""
    # Exclusão
    if request.GET.get('delete_preco'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM precos_convenio WHERE id = %s", [request.GET.get('delete_preco')])
        return HttpResponseRedirect('/precos/')

    # Cadastro
    if request.method == "POST":
        conv = request.POST.get('convenio_id')
        esp = request.POST.get('especialidade_id')
        valor = request.POST.get('valor')
        tuss = request.POST.get('tuss')
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO precos_convenio (convenio_id, especialidade_id, valor_pagamento, codigo_tuss) VALUES (%s, %s, %s, %s)",
                    [conv, esp, valor, tuss]
                )
            mensagem = '<div class="alert alert-success">✅ Preço configurado com sucesso!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    # Busca Dados para o Formulário e Tabela
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM convenios ORDER BY nome")
        lista_conv = cursor.fetchall()
        
        cursor.execute("SELECT id, nome FROM especialidades ORDER BY nome")
        lista_esp = cursor.fetchall()

        cursor.execute("""
            SELECT pr.id, c.nome, e.nome, pr.valor_pagamento, pr.codigo_tuss 
            FROM precos_convenio pr
            JOIN convenios c ON pr.convenio_id = c.id
            JOIN especialidades e ON pr.especialidade_id = e.id
            ORDER BY c.nome, e.nome
        """)
        tabela_precos = cursor.fetchall()

    opts_conv = "".join([f'<option value="{c[0]}">{c[1]}</option>' for c in lista_conv])
    opts_esp = "".join([f'<option value="{e[0]}">{e[1]}</option>' for e in lista_esp])
    
    linhas = "".join([f"""
        <tr>
            <td><b>{p[1]}</b></td>
            <td>{p[2]}</td>
            <td>R$ {p[3]}</td>
            <td><small>{p[4] if p[4] else '---'}</small></td>
            <td><a href="/precos/?delete_preco={p[0]}" class="btn btn-sm btn-danger" onclick="return confirm('Excluir?')"><i class="bi bi-trash"></i></a></td>
        </tr>""" for p in tabela_precos])

    conteudo = f"""
        <h4><i class="bi bi-currency-dollar"></i> Preços por Convênio</h4><hr>
        {mensagem}
        <form method="POST" class="row g-3 mb-4">
            <div class="col-md-4"><label class="form-label fw-bold">Convênio</label><select name="convenio_id" class="form-select" required>{opts_conv}</select></div>
            <div class="col-md-3"><label class="form-label fw-bold">Especialidade</label><select name="especialidade_id" class="form-select" required>{opts_esp}</select></div>
            <div class="col-md-2"><label class="form-label fw-bold">Valor (R$)</label><input type="number" step="0.01" name="valor" class="form-control" required></div>
            <div class="col-md-3"><label class="form-label fw-bold">Cód. TUSS (Opcional)</label><input type="text" name="tuss" class="form-control"></div>
            <div class="col-12"><button type="submit" class="btn btn-primary w-100 fw-bold">SALVAR TABELA DE PREÇO</button></div>
        </form>
        <hr>
        <div class="table-responsive">
            <table class="table table-hover mt-2">
                <thead class="table-dark"><tr><th>Convênio</th><th>Especialidade</th><th>Valor</th><th>TUSS</th><th>Ação</th></tr></thead>
                <tbody>{linhas if tabela_precos else '<tr><td colspan="5" class="text-center">Nenhum preço configurado.</td></tr>'}</tbody>
            </table>
        </div>
        <a href="/" class="btn btn-outline-secondary mt-3">⬅️ Voltar ao Painel</a>
    """
    return HttpResponse(base_html("Preços Convênio", conteudo))

# --- 13. TELA 10: PREÇOS DE EXAMES POR CONVÊNIO ---
@csrf_exempt
def precos_exames_geral(request):
    mensagem = ""
    # Exclusão
    if request.GET.get('delete_prexe'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM precos_exames WHERE id = %s", [request.GET.get('delete_prexe')])
        return HttpResponseRedirect('/precos-exames/')

    # Cadastro
    if request.method == "POST":
        conv = request.POST.get('convenio_id')
        exame = request.POST.get('exame_id')
        valor = request.POST.get('valor')
        tuss = request.POST.get('tuss')
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO precos_exames (convenio_id, exame_id, valor_convenio, codigo_tuss) VALUES (%s, %s, %s, %s)",
                    [conv, exame, valor, tuss]
                )
            mensagem = '<div class="alert alert-success">✅ Preço do exame salvo com sucesso!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    # Busca Dados
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM convenios ORDER BY nome")
        lista_conv = cursor.fetchall()
        
        cursor.execute("SELECT id, nome, grupo FROM exames ORDER BY grupo, nome")
        lista_exames = cursor.fetchall()

        cursor.execute("""
            SELECT px.id, c.nome, e.nome, px.valor_convenio, px.codigo_tuss, e.grupo 
            FROM precos_exames px
            JOIN convenios c ON px.convenio_id = c.id
            JOIN exames e ON px.exame_id = e.id
            ORDER BY c.nome, e.nome
        """)
        tabela_precos = cursor.fetchall()

    opts_conv = "".join([f'<option value="{c[0]}">{c[1]}</option>' for c in lista_conv])
    opts_ex = "".join([f'<option value="{e[0]}">[{e[2]}] {e[1]}</option>' for e in lista_exames])
    
    linhas = "".join([f"""
        <tr>
            <td><b>{p[1]}</b></td>
            <td>{p[2]} <br><small class='badge bg-light text-dark border'>{p[5]}</small></td>
            <td>R$ {p[3]}</td>
            <td>{p[4] if p[4] else '---'}</td>
            <td><a href="/precos-exames/?delete_prexe={p[0]}" class="btn btn-sm btn-danger" onclick="return confirm('Excluir?')"><i class="bi bi-trash"></i></a></td>
        </tr>""" for p in tabela_precos])

    conteudo = f"""
        <h4><i class="bi bi-tags"></i> Tabela de Preços: Exames</h4><hr>
        {mensagem}
        <form method="POST" class="row g-3 mb-4">
            <div class="col-md-4"><label class="form-label fw-bold">Convênio</label><select name="convenio_id" class="form-select" required>{opts_conv}</select></div>
            <div class="col-md-4"><label class="form-label fw-bold">Exame</label><select name="exame_id" class="form-select" required>{opts_ex}</select></div>
            <div class="col-md-2"><label class="form-label fw-bold">Valor (R$)</label><input type="number" step="0.01" name="valor" class="form-control" required></div>
            <div class="col-md-2"><label class="form-label fw-bold">Cód. TUSS</label><input type="text" name="tuss" class="form-control"></div>
            <div class="col-12"><button type="submit" class="btn btn-info w-100 fw-bold text-white shadow-sm">SALVAR TABELA DE EXAMES</button></div>
        </form>
        <hr>
        <div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-dark"><tr><th>Convênio</th><th>Exame / Grupo</th><th>Valor</th><th>TUSS</th><th>Ação</th></tr></thead>
                <tbody>{linhas if tabela_precos else '<tr><td colspan="5" class="text-center">Nenhum preço de exame configurado.</td></tr>'}</tbody>
            </table>
        </div>
        <a href="/" class="btn btn-outline-secondary mt-3">⬅️ Voltar ao Painel</a>
    """
    return HttpResponse(base_html("Preços Exames", conteudo))




# --- 14. TELA 11: CONFIGURAÇÃO DE AGENDAS (VERSÃO CORRIGIDA) ---
@csrf_exempt
def agendas_config_geral(request):
    mensagem = ""
    
    # Lógica de Exclusão
    if request.GET.get('delete_agenda'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM agendas_config WHERE id = %s", [request.GET.get('delete_agenda')])
        return HttpResponseRedirect('/agendas-config/')

    # Lógica de Cadastro (POST)
    if request.method == "POST":
        prof = request.POST.get('profissional_id')
        unid = request.POST.get('unidade_id')
        esp = request.POST.get('especialidade_id')
        tipo = request.POST.get('tipo_agenda')
        dia_semana = request.POST.get('dia_semana') if tipo == 'fixa' else None
        data_esp = request.POST.get('data_especifica') if tipo == 'especifica' else None
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')
        intervalo = request.POST.get('intervalo', 20)

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO agendas_config 
                       (profissional_id, unidade_id, especialidade_id, dia_semana, data_especifica, horario_inicio, horario_fim, intervalo_minutos) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    [prof, unid, esp, dia_semana, data_esp if data_esp else None, inicio, fim, intervalo]
                )
            mensagem = '<div class="alert alert-success">✅ Grade salva com sucesso!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro no banco: {e}</div>'

    # Busca de dados para os campos de seleção (Selects)
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM profissionais ORDER BY nome")
        profs = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unids = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM especialidades ORDER BY nome")
        esps = cursor.fetchall()
        
        # Lista das Agendas já criadas
        cursor.execute("""
            SELECT ac.id, p.nome, u.nome, ac.dia_semana, ac.data_especifica, 
                   ac.horario_inicio, ac.horario_fim, e.nome
            FROM agendas_config ac
            JOIN profissionais p ON ac.profissional_id = p.id
            JOIN unidades u ON ac.unidade_id = u.id
            JOIN especialidades e ON ac.especialidade_id = e.id
            ORDER BY ac.data_especifica DESC, ac.dia_semana ASC
        """)
        lista_agendas = cursor.fetchall()

    opts_prof = "".join([f'<option value="{p[0]}">{p[1]}</option>' for p in profs])
    opts_unid = "".join([f'<option value="{u[0]}">{u[1]}</option>' for u in unids])
    opts_esp = "".join([f'<option value="{e[0]}">{e[1]}</option>' for e in esps])
    
    # Montagem das linhas da tabela com tratamento para evitar NameError
    linhas = ""
    for a in lista_agendas:
        if a[3]: # Se tiver dia da semana
            quando = f"Toda {a[3]}"
        elif a[4]: # Se tiver data específica
            # Converte a data do banco para o formato brasileiro
            data_db = a[4]
            if isinstance(data_db, str):
                quando = datetime.datetime.strptime(data_db, '%Y-%m-%d').strftime('%d/%m/%Y')
            else:
                quando = data_db.strftime('%d/%m/%Y')
        else:
            quando = "Não definido"

        linhas += f"""
            <tr>
                <td><b>{a[1]}</b><br><small>{a[7]}</small></td>
                <td>{a[2]}</td>
                <td><span class="badge bg-secondary">{quando}</span></td>
                <td>{a[5]} - {a[6]}</td>
                <td><a href="/agendas-config/?delete_agenda={a[0]}" class="btn btn-sm btn-danger"><i class="bi bi-trash"></i></a></td>
            </tr>"""

    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4><i class="bi bi-calendar-plus"></i> Configuração de Grades</h4>
            <a href="/" class="btn btn-sm btn-outline-secondary">Voltar</a>
        </div>
        
        {mensagem}

        <form method="POST" class="card p-3 shadow-sm bg-light mb-4">
            <div class="row g-3">
                <div class="col-md-4">
                    <label class="fw-bold small">Profissional</label>
                    <select name="profissional_id" class="form-select" required>{opts_prof}</select>
                </div>
                <div class="col-md-4">
                    <label class="fw-bold small">Unidade</label>
                    <select name="unidade_id" class="form-select" required>{opts_unid}</select>
                </div>
                <div class="col-md-4">
                    <label class="fw-bold small">Especialidade</label>
                    <select name="especialidade_id" class="form-select" required>{opts_esp}</select>
                </div>

                <div class="col-md-3">
                    <label class="fw-bold small">Tipo de Grade</label>
                    <select name="tipo_agenda" id="tipo_agenda" class="form-select" onchange="alternarCampos()">
                        <option value="fixa">Repetir Semanalmente</option>
                        <option value="especifica">Data Única (Calendário)</option>
                    </select>
                </div>

                <div class="col-md-3" id="campo_semana">
                    <label class="fw-bold small">Dia da Semana</label>
                    <select name="dia_semana" class="form-select">
                        <option value="Segunda-feira">Segunda-feira</option>
                        <option value="Terça-feira">Terça-feira</option>
                        <option value="Quarta-feira">Quarta-feira</option>
                        <option value="Quinta-feira">Quinta-feira</option>
                        <option value="Sexta-feira">Sexta-feira</option>
                        <option value="Sábado">Sábado</option>
                    </select>
                </div>

                <div class="col-md-3" id="campo_data" style="display:none;">
                    <label class="fw-bold small">Selecione a Data</label>
                    <input type="date" name="data_especifica" class="form-control">
                </div>

                <div class="col-md-2">
                    <label class="fw-bold small">Início</label>
                    <input type="time" name="inicio" class="form-control" required>
                </div>
                <div class="col-md-2">
                    <label class="fw-bold small">Fim</label>
                    <input type="time" name="fim" class="form-control" required>
                </div>
                <div class="col-md-2">
                    <label class="fw-bold small">Intervalo (min)</label>
                    <input type="number" name="intervalo" class="form-control" value="20">
                </div>

                <div class="col-12 mt-3">
                    <button type="submit" class="btn btn-success w-100 fw-bold shadow-sm">SALVAR GRADE DE HORÁRIOS</button>
                </div>
            </div>
        </form>

        <script>
            function alternarCampos() {{
                var tipo = document.getElementById('tipo_agenda').value;
                document.getElementById('campo_semana').style.display = (tipo === 'fixa') ? 'block' : 'none';
                document.getElementById('campo_data').style.display = (tipo === 'especifica') ? 'block' : 'none';
            }}
        </script>

        <div class="table-responsive bg-white rounded shadow-sm">
            <table class="table table-hover mb-0">
                <thead class="table-dark">
                    <tr><th>Profissional</th><th>Unidade</th><th>Frequência</th><th>Horário</th><th>Ação</th></tr>
                </thead>
                <tbody>{linhas if linhas else '<tr><td colspan="5" class="text-center text-muted">Nenhuma grade configurada.</td></tr>'}</tbody>
            </table>
        </div>
    """
    return HttpResponse(base_html("Configuração de Agendas", conteudo))



# --- TELA 12 FINAL (COM LINK PARA AGENDAMENTO) ---
@csrf_exempt
def agenda_diaria(request):
    try:
        data_hoje = request.GET.get('data') or datetime.date.today().strftime('%Y-%m-%d')

        data_obj = datetime.datetime.strptime(data_hoje, '%Y-%m-%d')

        dias = ['Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado','Domingo']
        dia_semana = dias[data_obj.weekday()]

        horarios = []

        with connection.cursor() as cursor:

            # 🔹 BUSCAR AGENDAS
            cursor.execute("""
                SELECT ac.id, p.nome, ac.horario_inicio, ac.horario_fim, ac.intervalo_minutos
                FROM agendas_config ac
                JOIN profissionais p ON ac.profissional_id = p.id
                WHERE (ac.dia_semana = %s OR ac.data_especifica = %s)
            """, [dia_semana, data_hoje])

            agendas = cursor.fetchall()

            for ag in agendas:
                prof_nome = ag[1]
                inicio = ag[2]
                fim = ag[3]
                intervalo = ag[4] or 20

                # 🔥 CONVERSÃO SEGURA (resolve erro do banco)
                if isinstance(inicio, str):
                    inicio = datetime.datetime.strptime(inicio, '%H:%M:%S').time()
                if isinstance(fim, str):
                    fim = datetime.datetime.strptime(fim, '%H:%M:%S').time()

                hora_atual = datetime.datetime.combine(data_obj, inicio)

                while hora_atual.time() < fim:
                    horarios.append({
                        "hora": hora_atual.strftime('%H:%M'),
                        "profissional": prof_nome
                    })

                    hora_atual += datetime.timedelta(minutes=intervalo)

            # 🔹 BUSCAR AGENDAMENTOS
            cursor.execute("""
                SELECT horario_selecionado
                FROM agendamentos
                WHERE data_agendamento = %s
            """, [data_hoje])

            agendados_raw = cursor.fetchall()

            ocupados = set()

            for a in agendados_raw:
                hora = a[0]

                if isinstance(hora, str):
                    hora = datetime.datetime.strptime(hora, '%H:%M:%S').strftime('%H:%M')
                else:
                    hora = hora.strftime('%H:%M')

                ocupados.add(hora)

        # 🔹 MONTAR TABELA
        linhas = ""

        for h in sorted(horarios, key=lambda x: x['hora']):

            if h['hora'] in ocupados:
                status = "<span class='badge bg-danger'>Ocupado</span>"
                botao = f"""
                    <button class="btn btn-sm btn-danger" disabled>
                        {h['hora']}
                    </button>
                """
            else:
                status = "<span class='badge bg-success'>Livre</span>"
                botao = f"""
                    <a href="/agendar/?hora={h['hora']}&prof={h['profissional']}&data={data_hoje}" 
                       class="btn btn-sm btn-outline-primary">
                       {h['hora']}
                    </a>
                """

            linhas += f"""
                <tr>
                    <td>{botao}</td>
                    <td>{h['profissional']}</td>
                    <td>{status}</td>
                </tr>
            """

        conteudo = f"""
            <h4><i class="bi bi-calendar3"></i> Agenda do Dia</h4>

            <form method="GET" class="row mb-3">
                <div class="col-md-4">
                    <input type="date" name="data" value="{data_hoje}" class="form-control">
                </div>
                <div class="col-md-2">
                    <button class="btn btn-primary">Buscar</button>
                </div>
            </form>

            <div class="table-responsive">
                <table class="table table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Horário</th>
                            <th>Profissional</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {linhas if linhas else "<tr><td colspan='3' class='text-center'>Sem horários disponíveis</td></tr>"}
                    </tbody>
                </table>
            </div>
        """

        return HttpResponse(base_html("Agenda do Dia", conteudo))

    except Exception as e:
        return HttpResponse(base_html("Erro", f"<h4>Erro:</h4><pre>{e}</pre>"))


# --- TELA 13: AGENDAMENTO ---
@csrf_exempt
def agendar_consulta(request):

    data = request.GET.get('data')
    hora = request.GET.get('hora')
    prof_nome = request.GET.get('prof')

    mensagem = ""

    try:
        with connection.cursor() as cursor:

            # 🔹 Buscar ID do profissional
            cursor.execute("SELECT id FROM profissionais WHERE nome = %s", [prof_nome])
            prof = cursor.fetchone()
            profissional_id = prof[0] if prof else None

            # 🔹 Buscar especialidade e unidade
            cursor.execute("""
                SELECT e.nome, u.nome, e.id, u.id
                FROM agendas_config ac
                JOIN especialidades e ON ac.especialidade_id = e.id
                JOIN unidades u ON ac.unidade_id = u.id
                WHERE ac.profissional_id = %s
                LIMIT 1
            """, [profissional_id])

            dados = cursor.fetchone()

            especialidade = dados[0] if dados else ""
            unidade = dados[1] if dados else ""
            especialidade_id = dados[2] if dados else None

            # 🔹 Lista convênios
            cursor.execute("SELECT id, nome FROM convenios ORDER BY nome")
            convenios = cursor.fetchall()

    except Exception as e:
        return HttpResponse(base_html("Erro", f"<pre>{e}</pre>"))

    # 🔹 SALVAR AGENDAMENTO
    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        telefone = request.POST.get('telefone')
        convenio_id = request.POST.get('convenio')

        nome_completo = f"{nome} {sobrenome}"

        try:
            with connection.cursor() as cursor:

                # 🔹 cria paciente
                cursor.execute("""
                    INSERT INTO pacientes (nome, telefone, convenio_id)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, [nome_completo, telefone, convenio_id if convenio_id else None])

                paciente_id = cursor.fetchone()[0]

                # 🔹 cria agendamento
                cursor.execute("""
                    INSERT INTO agendamentos 
                    (paciente_id, agenda_config_id, data_agendamento, horario_selecionado, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, [paciente_id, profissional_id, data, hora, 'Agendado'])

            mensagem = "<div class='alert alert-success'>✅ Consulta agendada!</div>"

        except Exception as e:
            mensagem = f"<div class='alert alert-danger'>❌ Erro: {e}</div>"

    # 🔹 montar opções convênio
    opts_conv = "".join([f'<option value="{c[0]}">{c[1]}</option>' for c in convenios])

    conteudo = f"""
        <h4>Agendamento</h4>
        {mensagem}

        <div class="mb-3">
            <b>📅 Data:</b> {data} <br>
            <b>⏰ Hora:</b> {hora} <br>
            <b>👨‍⚕️ Médico:</b> {prof_nome} <br>
            <b>🏥 Unidade:</b> {unidade} <br>
            <b>🩺 Especialidade:</b> {especialidade}
        </div>

        <form method="POST" class="row g-3">

            <div class="col-md-6">
                <label>Nome</label>
                <input type="text" name="nome" class="form-control" required>
            </div>

            <div class="col-md-6">
                <label>Sobrenome</label>
                <input type="text" name="sobrenome" class="form-control">
            </div>

            <div class="col-md-6">
                <label>Telefone</label>
                <input type="text" name="telefone" class="form-control">
            </div>

            <div class="col-md-6">
                <label>Convênio</label>
                <select name="convenio" class="form-select">
                    <option value="">Particular</option>
                    {opts_conv}
                </select>
            </div>

            <div class="col-12">
                <button class="btn btn-success w-100">Confirmar Agendamento</button>
            </div>

        </form>
    """

    return HttpResponse(base_html("Agendar Consulta", conteudo))


# --- TELA 14: RECEPÇÃO ---
@csrf_exempt
def recepcao_geral(request):

    data_hoje = datetime.date.today().strftime('%Y-%m-%d')
    unidade_filtro = request.GET.get('unidade')

    mensagem = ""

    try:
        with connection.cursor() as cursor:

            # 🔹 Lista de unidades (filtro)
            cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
            unidades = cursor.fetchall()

            # 🔹 BUSCA AGENDAMENTOS DO DIA
            query = """
                SELECT 
                    ag.id,
                    p.nome,
                    pr.nome,
                    u.nome,
                    ag.horario_selecionado,
                    ag.status
                FROM agendamentos ag
                JOIN pacientes p ON ag.paciente_id = p.id
                JOIN agendas_config ac ON ag.agenda_config_id = ac.id
                JOIN profissionais pr ON ac.profissional_id = pr.id
                JOIN unidades u ON ac.unidade_id = u.id
                WHERE ag.data_agendamento = %s
            """

            params = [data_hoje]

            if unidade_filtro:
                query += " AND u.id = %s"
                params.append(unidade_filtro)

            query += " ORDER BY ag.horario_selecionado"

            cursor.execute(query, params)
            agenda = cursor.fetchall()

    except Exception as e:
        return HttpResponse(base_html("Erro", f"<pre>{e}</pre>"))

    # 🔹 ALTERAR STATUS
    if request.GET.get('acao'):
        ag_id = request.GET.get('id')
        acao = request.GET.get('acao')

        novo_status = "Aguardando"

        if acao == "chegada":
            novo_status = "Aguardando"
        elif acao == "atendimento":
            novo_status = "Em Atendimento"
        elif acao == "finalizar":
            novo_status = "Finalizado"

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE agendamentos
                SET status = %s
                WHERE id = %s
            """, [novo_status, ag_id])

        return HttpResponseRedirect('/recepcao/')

    # 🔹 Montar tabela
    linhas = ""

    for a in agenda:

        hora = a[4]
        if isinstance(hora, str):
            hora = datetime.datetime.strptime(hora, '%H:%M:%S').strftime('%H:%M')
        else:
            hora = hora.strftime('%H:%M')

        status = a[5] or "Aguardando"

        cor = {
            "Aguardando": "warning",
            "Em Atendimento": "primary",
            "Finalizado": "success"
        }.get(status, "secondary")

        linhas += f"""
            <tr>
                <td><b>{hora}</b></td>
                <td>{a[1]}</td>
                <td>{a[2]}</td>
                <td>{a[3]}</td>
                <td><span class="badge bg-{cor}">{status}</span></td>
                <td>
                    <a href="/recepcao/?acao=chegada&id={a[0]}" class="btn btn-sm btn-warning">Chegada</a>
                    <a href="/recepcao/?acao=atendimento&id={a[0]}" class="btn btn-sm btn-primary">Atender</a>
                    <a href="/recepcao/?acao=finalizar&id={a[0]}" class="btn btn-sm btn-success">Finalizar</a>
                </td>
            </tr>
        """

    # 🔹 Select unidades
    opts_unidades = "".join([f'<option value="{u[0]}">{u[1]}</option>' for u in unidades])

    conteudo = f"""
        <h4><i class="bi bi-person-check"></i> Recepção de Pacientes</h4>

        <form method="GET" class="row mb-3">
            <div class="col-md-4">
                <select name="unidade" class="form-select">
                    <option value="">Todas Unidades</option>
                    {opts_unidades}
                </select>
            </div>
            <div class="col-md-2">
                <button class="btn btn-primary">Filtrar</button>
            </div>
        </form>

        <div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Hora</th>
                        <th>Paciente</th>
                        <th>Profissional</th>
                        <th>Unidade</th>
                        <th>Status</th>
                        <th>Ação</th>
                    </tr>
                </thead>
                <tbody>
                    {linhas if linhas else "<tr><td colspan='6'>Sem pacientes hoje</td></tr>"}
                </tbody>
            </table>
        </div>
    """

    return HttpResponse(base_html("Recepção", conteudo))






# ---6. ROTAS ----
urlpatterns = [
    path('', painel_controle),              # Painel Geral
    path('unidades/', cadastro_unidade),    # Cadastro Unidades
    path('unidades/lista/', lista_unidades), # Lista Unidades
    path('especialidades/', especialidades_geral), # Especialidades
    path('profissionais/', profissionais_geral),   # Médicos/Dentistas
    path('convenios/', convenios_geral),           # <--- A NOVA TELA AQUI
    path('exames/', exames_geral),
    path('odontologia/', odonto_geral),
    path('pacientes/', pacientes_geral),
    path('acessos/', acesso_geral),
    path('precos/', precos_geral),
    path('precos-exames/', precos_exames_geral),
    path('agendas-config/', agendas_config_geral),
    path('agenda-diaria/', agenda_diaria),
    path('agendar/', agendar_consulta),
    path('recepcao/', recepcao_geral),
   
]
