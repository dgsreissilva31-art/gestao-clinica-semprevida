import datetime
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


# --- 1. TEMPLATE BASE (SIDEBAR COMPLETA E PROFISSIONAL) ---

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
            
            /* Topo */
            .navbar-top {{ background-color: var(--top-bg); height: 50px; position: fixed; width: 100%; top: 0; z-index: 1000; color: white; display: flex; align-items: center; padding: 0 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            
            /* Sidebar */
            .sidebar {{ background-color: var(--sidebar-bg); width: var(--sidebar-width); height: 100vh; position: fixed; top: 0; left: 0; padding-top: 50px; z-index: 999; overflow-y: auto; transition: all 0.3s; }}
            .sidebar-menu {{ list-style: none; padding: 0; margin: 0; }}
            .sidebar-menu li a {{ padding: 10px 15px; display: flex; align-items: center; color: #b8c7ce; text-decoration: none; border-left: 3px solid transparent; font-size: 14px; }}
            .sidebar-menu li a i {{ margin-right: 10px; width: 20px; text-align: center; }}
            .sidebar-menu li a:hover {{ background: #1e282c; color: white; border-left-color: #3c8dbc; }}
            
            /* Rótulos de Seção */
            .menu-label {{ padding: 12px 15px 5px; font-size: 11px; color: #4b646f; background: #1a2226; text-transform: uppercase; font-weight: bold; }}
            
            /* Conteúdo Principal */
            .main-content {{ margin-left: var(--sidebar-width); padding: 70px 20px 20px; min-height: 100vh; }}
            .card-panel {{ background: white; border-top: 3px solid #3c8dbc; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 20px; }}
            
            /* Responsividade */
            @media (max-width: 768px) {{ 
                .sidebar {{ left: -260px; }} 
                .main-content {{ margin-left: 0; }} 
                .sidebar.active {{ left: 0; }} 
            }}
        </style>
    </head>
    <body>
        <div class="navbar-top d-flex justify-content-between">
            <div>
                <i class="bi bi-list fs-4" style="cursor:pointer" onclick="document.querySelector('.sidebar').classList.toggle('active')"></i> 
                <span class="ms-2 fw-bold text-uppercase" style="letter-spacing: 1px;">SEMPRE VIDA</span>
            </div>
            <div class="small"><i class="bi bi-person-circle"></i> Douglas Silva</div>
        </div>

        <div class="sidebar shadow">
            <ul class="sidebar-menu">
                <div class="menu-label">Principal</div>
                <li><a href="/admin-painel/"><i class="bi bi-speedometer2"></i> Dashboard</a></li>
                
                <div class="menu-label">Operacional Hoje</div>
                <li><a href="/recepcao/"><i class="bi bi-person-check-fill"></i> Recepção / Check-in</a></li>
                <li><a href="/agendar/"><i class="bi bi-calendar-plus-fill"></i> Novo Agendamento</a></li>
                <li><a href="/caixa/"><i class="bi bi-cash-stack"></i> Caixa do Dia</a></li>
                <li><a href="/agenda-diaria/"><i class="bi bi-calendar3"></i> Agenda Geral</a></li>

                <div class="menu-label">Cadastros</div>
                <li><a href="/pacientes/"><i class="bi bi-people-fill"></i> Pacientes</a></li>
                <li><a href="/profissionais/"><i class="bi bi-person-md"></i> Profissionais</a></li>
                <li><a href="/unidades/"><i class="bi bi-building"></i> Unidades</a></li>
                <li><a href="/especialidades/"><i class="bi bi-hospital"></i> Especialidades</a></li>
                
                <div class="menu-label">Serviços e Preços</div>
                <li><a href="/convenios/"><i class="bi bi-card-checklist"></i> Convênios</a></li>
                <li><a href="/exames/"><i class="bi bi-microscope"></i> Exames</a></li>
                <li><a href="/odontologia/"><i class="bi bi-mask"></i> Odontologia</a></li>
                <li><a href="/precos/"><i class="bi bi-currency-dollar"></i> Preços Consultas</a></li>
                <li><a href="/precos-exames/"><i class="bi bi-tags-fill"></i> Preços Exames</a></li>

                <div class="menu-label">Configurações</div>
                <li><a href="/agendas-config/"><i class="bi bi-gear-fill"></i> Configurar Grades</a></li>
                <li><a href="/acessos/"><i class="bi bi-shield-lock-fill"></i> Acessos / Usuários</a></li>
                <hr style="border-color: #4b646f; margin: 10px 0;">
                <li><a href="/" class="text-info"><i class="bi bi-globe"></i> Visualizar Site</a></li>
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

# --- 2. TELA 0: PAINEL DE GESTÃO ---

# --- 2. TELA 0: PAINEL DE GESTÃO (VERSÃO PROFISSIONAL CORRIGIDA) ---

def painel_controle(request):
    # Definimos o conteúdo usando o grid system col-md-4 para 3 colunas perfeitas
    conteudo = """
        <div class="mb-4">
            <h3 class="fw-bold text-dark"><i class="bi bi-speedometer2 text-primary"></i> Painel de Gestão</h3>
            <p class="text-muted">Bem-vindo, Douglas Silva. Gerencie as operações da clínica Sempre Vida.</p>
        </div>
        
        <div class="row g-3">
            <div class="col-md-4">
                <div class="p-4 bg-primary text-white rounded shadow-sm text-center h-100">
                    <i class="bi bi-building fs-1"></i><br><h5 class="mt-2 fw-bold">Unidades</h5>
                    <a href="/unidades/" class="btn btn-sm btn-light mt-2 fw-bold w-100">Acessar</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-success text-white rounded shadow-sm text-center h-100">
                    <i class="bi bi-hospital fs-1"></i><br><h5 class="mt-2 fw-bold">Especialidades</h5>
                    <a href="/especialidades/" class="btn btn-sm btn-light mt-2 fw-bold w-100">Acessar</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-warning text-dark rounded shadow-sm text-center h-100">
                    <i class="bi bi-person-badge fs-1"></i><br><h5 class="mt-2 fw-bold">Profissionais</h5>
                    <a href="/profissionais/" class="btn btn-sm btn-dark mt-2 fw-bold w-100 text-white">Acessar</a>
                </div>
            </div>

            <div class="col-md-4">
                <div class="p-4 bg-info text-white rounded shadow-sm text-center h-100">
                    <i class="bi bi-card-checklist fs-1"></i><br><h5 class="mt-2 fw-bold">Convênios</h5>
                    <a href="/convenios/" class="btn btn-sm btn-light mt-2 fw-bold w-100">Acessar</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-secondary text-white rounded shadow-sm text-center h-100">
                    <i class="bi bi-microscope fs-1"></i><br><h5 class="mt-2 fw-bold">Exames</h5>
                    <a href="/exames/" class="btn btn-sm btn-light mt-2 fw-bold w-100">Acessar</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-dark text-white rounded shadow-sm text-center h-100">
                    <i class="bi bi-mask fs-1"></i><br><h5 class="mt-2 fw-bold">Odontologia</h5>
                    <a href="/odontologia/" class="btn btn-sm btn-light mt-2 fw-bold w-100">Acessar</a>
                </div>
            </div>

            <div class="col-md-4">
                <div class="p-4 bg-danger text-white rounded shadow-sm text-center h-100">
                    <i class="bi bi-people fs-1"></i><br><h5 class="mt-2 fw-bold">Pacientes</h5>
                    <a href="/pacientes/" class="btn btn-sm btn-light mt-2 fw-bold w-100">Acessar</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-dark text-white rounded shadow-sm text-center h-100 border-secondary border">
                    <i class="bi bi-shield-lock fs-1"></i><br><h5 class="mt-2 fw-bold">Acessos</h5>
                    <a href="/acessos/" class="btn btn-sm btn-light mt-2 fw-bold w-100">Configurar</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-primary text-white rounded shadow-sm text-center h-100 border-light border">
                    <i class="bi bi-currency-dollar fs-1"></i><br><h5 class="mt-2 fw-bold">Tabela de Preços</h5>
                    <a href="/precos/" class="btn btn-sm btn-light mt-2 fw-bold w-100">Configurar</a>
                </div>
            </div>

            <div class="col-md-4">
                <div class="p-4 bg-info text-white rounded shadow-sm text-center h-100">
                    <i class="bi bi-tags fs-1"></i><br><h5 class="mt-2 fw-bold">Preços Exames</h5>
                    <a href="/precos-exames/" class="btn btn-sm btn-light mt-2 fw-bold w-100">Configurar</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-success text-white rounded shadow-sm text-center h-100">
                    <i class="bi bi-calendar-check fs-1"></i><br><h5 class="mt-2 fw-bold">Configurar Agendas</h5>
                    <a href="/agendas-config/" class="btn btn-sm btn-light mt-2 fw-bold w-100">Configurar</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-white text-dark rounded shadow-sm text-center h-100 border border-primary">
                    <i class="bi bi-calendar-plus fs-1 text-primary"></i><br><h5 class="mt-2 fw-bold text-primary">Novo Agendamento</h5>
                    <a href="/agendar/" class="btn btn-sm btn-primary mt-2 fw-bold w-100 text-white">Iniciar</a>
                </div>
            </div>

            <div class="col-md-4">
                <div class="p-4 bg-warning text-dark rounded shadow-sm text-center h-100 border border-dark">
                    <i class="bi bi-person-check fs-1"></i><br><h5 class="mt-2 fw-bold">Recepção / Check-in</h5>
                    <a href="/recepcao/" class="btn btn-sm btn-dark mt-2 fw-bold w-100 text-white">Abrir Painel</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-light text-dark rounded shadow-sm text-center h-100 border">
                    <i class="bi bi-cash-stack fs-1 text-success"></i><br><h5 class="mt-2 fw-bold">Caixa / Financeiro</h5>
                    <a href="/caixa/" class="btn btn-sm btn-success mt-2 fw-bold w-100">Abrir Caixa</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="p-4 bg-white text-dark rounded shadow-sm text-center h-100 border">
                    <i class="bi bi-file-earmark-medical fs-1 text-purple" style="color: #605ca8;"></i><br><h5 class="mt-2 fw-bold">Prontuário Médico</h5>
                    <a href="/recepcao/" class="btn btn-sm btn-outline-dark mt-2 fw-bold w-100">Atender</a>
                </div>
            </div>
        </div>
    """
    return HttpResponse(base_html("Dashboard", conteudo))



    


# --- 3. TELA 1: UNIDADES ---
@csrf_exempt
def cadastro_unidade(request):
    mensagem = ""
    # Se vier um ID via GET, estamos em modo EDIÇÃO
    edit_id = request.GET.get('edit')
    unidade_data = [None, "", "", ""] # ID, Nome, Endereco, Telefone

    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome, endereco, telefone FROM unidades WHERE id = %s", [edit_id])
            unidade_data = cursor.fetchone() or unidade_data

    if request.method == "POST":
        id_post = request.POST.get('id_unidade')
        nome = request.POST.get('nome')
        end = request.POST.get('endereco')
        tel = request.POST.get('telefone')
        
        try:
            with connection.cursor() as cursor:
                if id_post: # UPDATE
                    cursor.execute("""
                        UPDATE unidades SET nome=%s, endereco=%s, telefone=%s WHERE id=%s
                    """, [nome, end, tel, id_post])
                    mensagem = '<div class="alert alert-success">✅ Unidade Atualizada!</div>'
                else: # INSERT
                    cursor.execute("""
                        INSERT INTO unidades (nome, endereco, telefone) VALUES (%s, %s, %s)
                    """, [nome, end, tel])
                    mensagem = '<div class="alert alert-success">✅ Unidade Salva!</div>'
            return HttpResponseRedirect('/unidades/lista/')
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'
    
    conteudo = f"""
        <h4><i class="bi bi-pencil-square"></i> {"Editar" if edit_id else "Nova"} Unidade</h4><hr>
        {mensagem}
        <form method="POST" class="row g-3">
            <input type="hidden" name="id_unidade" value="{unidade_data[0] or ''}">
            <div class="col-md-6">
                <label class="form-label fw-bold">Nome</label>
                <input type="text" name="nome" class="form-control" value="{unidade_data[1]}" required>
            </div>
            <div class="col-md-6">
                <label class="form-label fw-bold">Telefone</label>
                <input type="text" name="telefone" class="form-control" value="{unidade_data[3]}">
            </div>
            <div class="col-12">
                <label class="form-label fw-bold">Endereço</label>
                <input type="text" name="endereco" class="form-control" value="{unidade_data[2]}">
            </div>
            <div class="col-12">
                <button type="submit" class="btn btn-primary">{"Atualizar" if edit_id else "Salvar"}</button>
                <a href="/unidades/lista/" class="btn btn-outline-dark">Cancelar / Listar</a>
            </div>
        </form>
    """
    return HttpResponse(base_html("Unidades", conteudo))

def lista_unidades(request):
    if request.GET.get('delete'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM unidades WHERE id = %s", [request.GET.get('delete')])
        return HttpResponseRedirect('/unidades/lista/')

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, endereco, telefone FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()

    # MONTAGEM DAS LINHAS COM O BOTÃO DE ALTERAR (AZUL)
    linhas = ""
    for u in unidades:
        linhas += f"""
        <tr>
            <td>{u[1]}</td>
            <td>{u[2]}</td>
            <td>{u[3] or '---'}</td>
            <td>
                <div class="btn-group">
                    <a href="/unidades/?edit={u[0]}" class="btn btn-sm btn-info text-white" title="Alterar">
                        <i class="bi bi-pencil"></i>
                    </a>
                    <a href="/unidades/lista/?delete={u[0]}" class="btn btn-sm btn-danger" 
                       onclick="return confirm('Deseja excluir?')" title="Excluir">
                        <i class="bi bi-trash"></i>
                    </a>
                </div>
            </td>
        </tr>"""

    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4>Unidades Ativas</h4>
            <a href='/unidades/' class='btn btn-primary'><i class="bi bi-plus-lg"></i> Nova Unidade</a>
        </div>
        <hr>
        <table class='table table-hover'>
            <thead class='table-light'>
                <tr><th>Nome</th><th>Endereço</th><th>Telefone</th><th>Ação</th></tr>
            </thead>
            <tbody>{linhas if unidades else "<tr><td colspan='4' class='text-center'>Nenhuma unidade.</td></tr>"}</tbody>
        </table>
        <a href='/unidades/' class='btn btn-outline-secondary'>Voltar</a>
    """
    return HttpResponse(base_html("Lista Unidades", conteudo))






# --- 4. TELA 2: ESPECIALIDADES ---
@csrf_exempt
def especialidades_geral(request):
    mensagem = ""
    # 1. Lógica de Exclusão
    if request.GET.get('delete_esp'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM especialidades WHERE id = %s", [request.GET.get('delete_esp')])
        return HttpResponseRedirect('/especialidades/')

    # 2. Lógica para Carregar Dados de Edição
    edit_id = request.GET.get('edit_esp')
    esp_nome = ""
    esp_tipo = "Médica"
    
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nome, tipo FROM especialidades WHERE id = %s", [edit_id])
            res = cursor.fetchone()
            if res:
                esp_nome, esp_tipo = res

    # 3. Lógica de Salvar (Novo ou Alteração)
    if request.method == "POST":
        id_post = request.POST.get('id_esp')
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        
        with connection.cursor() as cursor:
            if id_post: # Se tem ID, atualiza
                cursor.execute("UPDATE especialidades SET nome=%s, tipo=%s WHERE id=%s", [nome, tipo, id_post])
            else: # Se não tem, insere novo
                cursor.execute("INSERT INTO especialidades (nome, tipo) VALUES (%s, %s)", [nome, tipo])
        return HttpResponseRedirect('/especialidades/')

    # 4. Busca Lista para a Tabela
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, tipo FROM especialidades ORDER BY tipo, nome")
        dados = cursor.fetchall()

    # 5. Montagem das Linhas com o Botão de Alterar (Lápis)
    itens = ""
    for d in dados:
        itens += f"""
        <tr>
            <td>{d[1]}</td>
            <td>{d[2]}</td>
            <td>
                <div class="btn-group">
                    <a href="/especialidades/?edit_esp={d[0]}" class="btn btn-sm btn-info text-white" title="Alterar">
                        <i class="bi bi-pencil"></i>
                    </a>
                    <a href="/especialidades/?delete_esp={d[0]}" class="btn btn-sm btn-danger" 
                       onclick="return confirm('Deseja excluir?')" title="Excluir">
                        <i class="bi bi-trash"></i>
                    </a>
                </div>
            </td>
        </tr>"""

    # 6. HTML da Página
    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center">
            <h4><i class="bi bi-hospital"></i> Especialidades</h4>
            <a href="/admin-painel/" class="btn btn-sm btn-outline-secondary">Voltar ao Dashboard</a>
        </div>
        <hr>
        
        <form method='POST' class='row g-2 mb-4 bg-light p-3 rounded border'>
            <input type="hidden" name="id_esp" value="{edit_id or ''}">
            <div class='col-md-6'>
                <label class="small fw-bold">Nome da Especialidade</label>
                <input type='text' name='nome' class='form-control' value="{esp_nome}" placeholder='Ex: Cardiologia' required>
            </div>
            <div class='col-md-4'>
                <label class="small fw-bold">Tipo</label>
                <select name='tipo' class='form-select'>
                    <option value='Médica' {"selected" if esp_tipo == "Médica" else ""}>Médica</option>
                    <option value='Odontológica' {"selected" if esp_tipo == "Odontológica" else ""}>Odontológica</option>
                </select>
            </div>
            <div class='col-md-2 d-flex align-items-end'>
                <button type='submit' class='btn btn-primary w-100 fw-bold'>
                    { '<i class="bi bi-check-lg"></i> Atualizar' if edit_id else '<i class="bi bi-plus-lg"></i> Salvar' }
                </button>
            </div>
            { f'<div class="col-12 mt-2"><a href="/especialidades/" class="small text-danger text-decoration-none">Cancelar Edição</a></div>' if edit_id else '' }
        </form>

        <div class="table-responsive">
            <table class='table table-sm table-hover'>
                <thead class='table-dark'>
                    <tr><th>Nome</th><th>Tipo</th><th>Ações</th></tr>
                </thead>
                <tbody>{itens if dados else '<tr><td colspan="3" class="text-center">Nenhuma cadastrada.</td></tr>'}</tbody>
            </table>
        </div>
    """
    return HttpResponse(base_html("Especialidades", conteudo))





# --- 5. TELA 3: PROFISSIONAIS ---
# --- 5. TELA 3: PROFISSIONAIS (UNIDADE PRIMEIRO NO FORMULÁRIO) ---
@csrf_exempt
def profissionais_geral(request):
    mensagem = ""
    
    # 1. Lógica de Exclusão
    if request.GET.get('delete_prof'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM profissionais WHERE id = %s", [request.GET.get('delete_prof')])
        return HttpResponseRedirect('/profissionais/')

    # 2. Carregar Dados para Edição
    edit_id = request.GET.get('edit_prof')
    p_dados = ["", "CRM", "", "", "", "", ""] 
    
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT nome, conselho_tipo, conselho_numero, especialidade_id, telefone, endereco, unidade_id 
                FROM profissionais WHERE id = %s
            """, [edit_id])
            res = cursor.fetchone()
            if res: p_dados = res

    # 3. Lógica de Salvar
    if request.method == "POST":
        id_post = request.POST.get('id_prof')
        nome = request.POST.get('nome')
        tipo = request.POST.get('tipo')
        num = request.POST.get('numero')
        esp = request.POST.get('especialidade_id')
        tel = request.POST.get('telefone')
        end = request.POST.get('endereco')
        unid = request.POST.get('unidade_id') or None
        
        try:
            with connection.cursor() as cursor:
                if id_post:
                    cursor.execute("""
                        UPDATE profissionais 
                        SET nome=%s, conselho_tipo=%s, conselho_numero=%s, especialidade_id=%s, 
                            telefone=%s, endereco=%s, unidade_id=%s
                        WHERE id=%s
                    """, [nome, tipo, num, esp, tel, end, unid, id_post])
                else:
                    cursor.execute("""
                        INSERT INTO profissionais (nome, conselho_tipo, conselho_numero, especialidade_id, telefone, endereco, unidade_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, [nome, tipo, num, esp, tel, end, unid])
            return HttpResponseRedirect('/profissionais/')
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    # 4. Busca de Dados
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM especialidades ORDER BY nome")
        especialidades = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()
        cursor.execute("""
            SELECT p.id, p.nome, p.conselho_tipo, p.conselho_numero, e.nome, p.telefone, u.nome 
            FROM profissionais p 
            LEFT JOIN especialidades e ON p.especialidade_id = e.id 
            LEFT JOIN unidades u ON p.unidade_id = u.id
            ORDER BY u.nome, p.nome
        """)
        profs = cursor.fetchall()

    opcoes_esp = "".join([f'<option value="{e[0]}" {"selected" if str(e[0])==str(p_dados[3]) else ""}>{e[1]}</option>' for e in especialidades])
    opcoes_unid = "".join([f'<option value="{u[0]}" {"selected" if str(u[0])==str(p_dados[6]) else ""}>{u[1]}</option>' for u in unidades])
    
    linhas = "".join([f"""
        <tr>
            <td><span class='badge bg-primary'>{p[6] if p[6] else 'Sem Unidade'}</span><br><b>{p[1]}</b></td>
            <td><span class="badge bg-secondary">{p[2]}</span> {p[3]}</td>
            <td>{p[4] if p[4] else "---"}</td>
            <td>{p[5] if p[5] else "---"}</td>
            <td>
                <div class="btn-group">
                    <a href="/profissionais/?edit_prof={p[0]}" class="btn btn-sm btn-info text-white"><i class="bi bi-pencil"></i></a>
                    <a href="/profissionais/?delete_prof={p[0]}" class="btn btn-sm btn-danger" onclick="return confirm('Excluir?')"><i class="bi bi-trash"></i></a>
                </div>
            </td>
        </tr>""" for p in profs])

    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center">
            <h4><i class="bi bi-person-badge"></i> Cadastro de Profissionais</h4>
            <a href="/admin-painel/" class="btn btn-sm btn-outline-secondary">Voltar ao Painel</a>
        </div>
        <hr>
        {mensagem}
        
        <form method='POST' class='row g-3 mb-4 bg-light p-3 rounded border shadow-sm'>
            <input type="hidden" name="id_prof" value="{edit_id or ''}">
            
            <div class='col-md-4'>
                <label class='small fw-bold text-primary'>1º Unidade Principal</label>
                <select name='unidade_id' class='form-select border-primary' required>
                    <option value="">-- Selecione a Unidade --</option>
                    {opcoes_unid}
                </select>
            </div>

            <div class='col-md-5'>
                <label class='small fw-bold'>2º Nome Completo</label>
                <input type='text' name='nome' class='form-control' value="{p_dados[0]}" required>
            </div>

            <div class='col-md-3'>
                <label class='small fw-bold'>Especialidade</label>
                <select name='especialidade_id' class='form-select'>{opcoes_esp}</select>
            </div>
            
            <div class='col-md-2'>
                <label class='small fw-bold'>Conselho</label>
                <select name='tipo' class='form-select'>
                    <option value='CRM' {"selected" if p_dados[1] == "CRM" else ""}>CRM</option>
                    <option value='CRO' {"selected" if p_dados[1] == "CRO" else ""}>CRO</option>
                </select>
            </div>
            
            <div class='col-md-3'>
                <label class='small fw-bold text-danger'>Número do Registro</label>
                <input type='text' name='numero' class='form-control' value="{p_dados[2]}" required>
            </div>
            
            <div class='col-md-3'>
                <label class='small fw-bold'>Telefone</label>
                <input type='text' name='telefone' class='form-control' value="{p_dados[4]}" placeholder='(00) 00000-0000'>
            </div>
            
            <div class='col-md-4'>
                <label class='small fw-bold'>Endereço</label>
                <input type='text' name='endereco' class='form-control' value="{p_dados[5]}">
            </div>
            
            <div class='col-12 mt-3'>
                <button type='submit' class='btn btn-primary w-100 fw-bold py-2 shadow'>
                    { 'ATUALIZAR PROFISSIONAL' if edit_id else 'SALVAR PROFISSIONAL' }
                </button>
            </div>
            { f'<div class="col-12 text-center mt-1"><a href="/profissionais/" class="text-muted small">Cancelar Edição</a></div>' if edit_id else '' }
        </form>
        
        <div class='table-responsive bg-white rounded shadow-sm p-2 border'>
            <table class='table table-hover align-middle mb-0'>
                <thead class='table-dark'>
                    <tr><th>Unidade / Nome</th><th>Registro</th><th>Especialidade</th><th>Telefone</th><th>Ação</th></tr>
                </thead>
                <tbody>{linhas if profs else '<tr><td colspan="5" class="text-center py-4">Nenhum profissional cadastrado.</td></tr>'}</tbody>
            </table>
        </div>
    """
    return HttpResponse(base_html("Profissionais", conteudo))




# --- 7. TELA 4: GESTÃO DE CONVÊNIOS ---
# --- 6. TELA 4: GESTÃO DE CONVÊNIOS (ATUALIZADA COM RESPONSÁVEL E ALTERAR) ---
@csrf_exempt
def convenios_geral(request):
    mensagem = ""
    
    # 1. Lógica de Exclusão
    if request.GET.get('delete_conv'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM convenios WHERE id = %s", [request.GET.get('delete_conv')])
        return HttpResponseRedirect('/convenios/')

    # 2. Lógica para Carregar Dados de Edição (Modo Alterar)
    edit_id = request.GET.get('edit_conv')
    c_dados = ["", "", "", "", ""] # nome, ans, tel, end, responsavel
    
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT nome, registro_ans, telefone_contato, endereco_completo, responsavel 
                FROM convenios WHERE id = %s
            """, [edit_id])
            res = cursor.fetchone()
            if res:
                c_dados = res

    # 3. Lógica de Salvar (Novo ou Alteração)
    if request.method == "POST":
        id_post = request.POST.get('id_conv')
        nome = request.POST.get('nome')
        ans = request.POST.get('ans')
        tel = request.POST.get('telefone')
        end = request.POST.get('endereco')
        resp = request.POST.get('responsavel')
        
        try:
            with connection.cursor() as cursor:
                if id_post: # UPDATE
                    cursor.execute("""
                        UPDATE convenios 
                        SET nome=%s, registro_ans=%s, telefone_contato=%s, endereco_completo=%s, responsavel=%s
                        WHERE id=%s
                    """, [nome, ans, tel, end, resp, id_post])
                    mensagem = '<div class="alert alert-success">✅ Convênio atualizado com sucesso!</div>'
                else: # INSERT
                    cursor.execute("""
                        INSERT INTO convenios (nome, registro_ans, telefone_contato, endereco_completo, responsavel) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, [nome, ans, tel, end, resp])
                    mensagem = '<div class="alert alert-success">✅ Convênio cadastrado com sucesso!</div>'
            return HttpResponseRedirect('/convenios/')
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    # 4. Busca Lista de Convênios
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, registro_ans, telefone_contato, endereco_completo, responsavel FROM convenios ORDER BY nome")
        conves = cursor.fetchall()

    # 5. Montagem das Linhas com Botão Alterar
    linhas = ""
    for c in conves:
        linhas += f"""
        <tr>
            <td><b>{c[1]}</b><br><small class='text-muted'>📍 {c[4] if c[4] else '---'}</small></td>
            <td>{c[2] if c[2] else '---'}</td>
            <td><b>Resp:</b> {c[5] if c[5] else '---'}<br><small>{c[3] if c[3] else '---'}</small></td>
            <td>
                <div class="btn-group">
                    <a href="/convenios/?edit_conv={c[0]}" class="btn btn-sm btn-info text-white" title="Alterar">
                        <i class="bi bi-pencil"></i>
                    </a>
                    <a href="/convenios/?delete_conv={c[0]}" class="btn btn-sm btn-danger" 
                       onclick="return confirm('Deseja excluir este convênio?')" title="Excluir">
                        <i class="bi bi-trash"></i>
                    </a>
                </div>
            </td>
        </tr>"""

    # 6. HTML da Página
    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center">
            <h4><i class="bi bi-card-checklist"></i> Cadastro de Convênios</h4>
            <a href="/admin-painel/" class="btn btn-sm btn-outline-secondary">Voltar ao Dashboard</a>
        </div>
        <hr>
        
        {mensagem}
        
        <form method="POST" class="row g-3 mb-4 bg-light p-3 rounded border shadow-sm">
            <input type="hidden" name="id_conv" value="{edit_id or ''}">
            
            <div class="col-md-5">
                <label class="form-label fw-bold small">Nome do Convênio</label>
                <input type="text" name="nome" class="form-control" value="{c_dados[0]}" placeholder="Ex: Unimed, Bradesco..." required>
            </div>
            
            <div class="col-md-3">
                <label class="form-label fw-bold small">Registro ANS</label>
                <input type="text" name="ans" class="form-control" value="{c_dados[1]}" placeholder="Cód. ANS">
            </div>

            <div class="col-md-4">
                <label class="form-label fw-bold small">Responsável na Operadora</label>
                <input type="text" name="responsavel" class="form-control" value="{c_dados[4]}" placeholder="Nome do consultor">
            </div>

            <div class="col-md-4">
                <label class="form-label fw-bold small">Telefone Suporte</label>
                <input type="text" name="telefone" class="form-control" value="{c_dados[2]}" placeholder="(00) 0000-0000">
            </div>

            <div class="col-md-8">
                <label class="form-label fw-bold small">Endereço da Operadora</label>
                <input type="text" name="endereco" class="form-control" value="{c_dados[3]}" placeholder="Rua, número, cidade...">
            </div>

            <div class="col-12">
                <button type="submit" class="btn btn-info w-100 fw-bold text-white shadow-sm">
                    { '<i class="bi bi-check-lg"></i> ATUALIZAR CONVÊNIO' if edit_id else '<i class="bi bi-plus-lg"></i> SALVAR CONVÊNIO' }
                </button>
            </div>
            { f'<div class="col-12 text-center mt-2"><a href="/convenios/" class="text-danger small text-decoration-none">Cancelar Edição</a></div>' if edit_id else '' }
        </form>

        <hr>
        <h5>Convênios Ativos</h5>
        <div class="table-responsive">
            <table class="table table-hover align-middle mt-2">
                <thead class="table-dark">
                    <tr><th>Nome / Endereço</th><th>ANS</th><th>Contato / Resp.</th><th>Ação</th></tr>
                </thead>
                <tbody>{linhas if conves else '<tr><td colspan="4" class="text-center text-muted py-4">Nenhum convênio cadastrado.</td></tr>'}</tbody>
            </table>
        </div>
    """
    return HttpResponse(base_html("Convênios", conteudo))







# --- 8. TELA 5: GESTÃO DE EXAMES (ATUALIZADA COM GRUPO) ---
# --- 8. TELA 5: GESTÃO DE EXAMES (ATUALIZADA COM ALTERAR) ---
@csrf_exempt
def exames_geral(request):
    mensagem = ""
    
    # 1. Lógica de Exclusão
    if request.GET.get('delete_exame'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM exames WHERE id = %s", [request.GET.get('delete_exame')])
        return HttpResponseRedirect('/exames/')

    # 2. Lógica para Carregar Dados de Edição (Modo Alterar)
    edit_id = request.GET.get('edit_exame')
    e_dados = ["", "", "", 0.00] # nome, grupo, preparo, valor
    
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT nome, grupo, preparo, valor_particular 
                FROM exames WHERE id = %s
            """, [edit_id])
            res = cursor.fetchone()
            if res:
                e_dados = res

    # 3. Lógica de Salvar (Novo ou Alteração)
    if request.method == "POST":
        id_post = request.POST.get('id_exame')
        nome = request.POST.get('nome')
        grupo = request.POST.get('grupo')
        preparo = request.POST.get('preparo')
        valor = request.POST.get('valor')
        
        try:
            with connection.cursor() as cursor:
                if id_post: # UPDATE
                    cursor.execute("""
                        UPDATE exames 
                        SET nome=%s, grupo=%s, preparo=%s, valor_particular=%s
                        WHERE id=%s
                    """, [nome, grupo, preparo, valor if valor else 0, id_post])
                    mensagem = '<div class="alert alert-success">✅ Exame atualizado com sucesso!</div>'
                else: # INSERT
                    cursor.execute("""
                        INSERT INTO exames (nome, grupo, preparo, valor_particular) 
                        VALUES (%s, %s, %s, %s)
                    """, [nome, grupo, preparo, valor if valor else 0])
                    mensagem = '<div class="alert alert-success">✅ Exame cadastrado com sucesso!</div>'
            return HttpResponseRedirect('/exames/')
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    # 4. Busca Lista de Exames
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, preparo, valor_particular, grupo FROM exames ORDER BY grupo, nome")
        exames_lista = cursor.fetchall()

    # 5. Montagem das Linhas com Botão Alterar
    linhas = ""
    for ex in exames_lista:
        linhas += f"""
        <tr>
            <td><b>{ex[1]}</b><br><span class="badge bg-light text-dark border">{ex[4] if ex[4] else 'Geral'}</span></td>
            <td><small>{ex[2] if ex[2] else 'Sem preparo específico.'}</small></td>
            <td>R$ {ex[3]}</td>
            <td>
                <div class="btn-group">
                    <a href="/exames/?edit_exame={ex[0]}" class="btn btn-sm btn-info text-white" title="Alterar">
                        <i class="bi bi-pencil"></i>
                    </a>
                    <a href="/exames/?delete_exame={ex[0]}" class="btn btn-sm btn-danger" 
                       onclick="return confirm('Excluir este exame?')" title="Excluir">
                        <i class="bi bi-trash"></i>
                    </a>
                </div>
            </td>
        </tr>"""

    # 6. HTML da Página
    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center">
            <h4><i class="bi bi-microscope"></i> Cadastro de Exames</h4>
            <a href="/admin-painel/" class="btn btn-sm btn-outline-secondary">Voltar ao Dashboard</a>
        </div>
        <hr>
        
        {mensagem}
        
        <form method="POST" class="row g-3 mb-4 bg-light p-3 rounded border shadow-sm">
            <input type="hidden" name="id_exame" value="{edit_id or ''}">
            
            <div class="col-md-5">
                <label class="form-label fw-bold small">Nome do Exame</label>
                <input type="text" name="nome" class="form-control" value="{e_dados[0]}" placeholder="Ex: Hemograma" required>
            </div>
            
            <div class="col-md-4">
                <label class="form-label fw-bold small">Grupo / Categoria</label>
                <input type="text" name="grupo" class="form-control" value="{e_dados[1]}" placeholder="Ex: Sangue, Imagem...">
            </div>

            <div class="col-md-3">
                <label class="form-label fw-bold small">Valor Particular (R$)</label>
                <input type="number" step="0.01" name="valor" class="form-control" value="{e_dados[3]}" placeholder="0.00">
            </div>

            <div class="col-12">
                <label class="form-label fw-bold small">Instruções de Preparo</label>
                <textarea name="preparo" class="form-control" rows="2" placeholder="Ex: Jejum de 8 horas...">{e_dados[2]}</textarea>
            </div>

            <div class="col-12">
                <button type="submit" class="btn btn-secondary w-100 fw-bold shadow-sm">
                    { '<i class="bi bi-check-lg"></i> ATUALIZAR EXAME' if edit_id else '<i class="bi bi-plus-lg"></i> SALVAR EXAME' }
                </button>
            </div>
            { f'<div class="col-12 text-center mt-2"><a href="/exames/" class="text-danger small text-decoration-none">Cancelar Edição</a></div>' if edit_id else '' }
        </form>

        <hr>
        <h5>Lista de Exames Cadastrados</h5>
        <div class="table-responsive">
            <table class="table table-hover align-middle mt-2">
                <thead class="table-dark">
                    <tr><th>Exame / Grupo</th><th>Preparo</th><th>Valor</th><th>Ações</th></tr>
                </thead>
                <tbody>{linhas if exames_lista else '<tr><td colspan="4" class="text-center text-muted py-4">Nenhum exame cadastrado.</td></tr>'}</tbody>
            </table>
        </div>
    """
    return HttpResponse(base_html("Exames", conteudo))








# --- 9. TELA 6: GESTÃO DE ODONTOLOGIA ---
# --- 9. TELA 6: GESTÃO DE ODONTOLOGIA (ATUALIZADA COM ALTERAR) ---
@csrf_exempt
def odonto_geral(request):
    mensagem = ""
    
    # 1. Lógica de Exclusão
    if request.GET.get('delete_odonto'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM odontologia WHERE id = %s", [request.GET.get('delete_odonto')])
        return HttpResponseRedirect('/odontologia/')

    # 2. Lógica para Carregar Dados de Edição (Modo Alterar)
    edit_id = request.GET.get('edit_odonto')
    o_dados = ["", "", 0.00, ""] # procedimento, grupo, valor, observacoes
    
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT procedimento, grupo, valor_particular, observacoes 
                FROM odontologia WHERE id = %s
            """, [edit_id])
            res = cursor.fetchone()
            if res:
                o_dados = res

    # 3. Lógica de Salvar (Novo ou Alteração)
    if request.method == "POST":
        id_post = request.POST.get('id_odonto')
        proc = request.POST.get('procedimento')
        grupo = request.POST.get('grupo')
        valor = request.POST.get('valor')
        obs = request.POST.get('observacoes')
        
        try:
            with connection.cursor() as cursor:
                if id_post: # UPDATE
                    cursor.execute("""
                        UPDATE odontologia 
                        SET procedimento=%s, grupo=%s, valor_particular=%s, observacoes=%s
                        WHERE id=%s
                    """, [proc, grupo, valor if valor else 0, obs, id_post])
                    mensagem = '<div class="alert alert-success">✅ Procedimento atualizado com sucesso!</div>'
                else: # INSERT
                    cursor.execute("""
                        INSERT INTO odontologia (procedimento, grupo, valor_particular, observacoes) 
                        VALUES (%s, %s, %s, %s)
                    """, [proc, grupo, valor if valor else 0, obs])
                    mensagem = '<div class="alert alert-success">✅ Procedimento salvo com sucesso!</div>'
            return HttpResponseRedirect('/odontologia/')
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    # 4. Busca Lista
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, procedimento, grupo, valor_particular, observacoes FROM odontologia ORDER BY grupo, procedimento")
        lista_odonto = cursor.fetchall()

    # 5. Montagem das Linhas com Botão Alterar
    linhas = ""
    for o in lista_odonto:
        linhas += f"""
        <tr>
            <td><b>{o[1]}</b><br><span class="badge bg-light text-dark border">{o[2] if o[2] else 'Geral'}</span></td>
            <td>R$ {o[3]}</td>
            <td><small>{o[4] if o[4] else '---'}</small></td>
            <td>
                <div class="btn-group">
                    <a href="/odontologia/?edit_odonto={o[0]}" class="btn btn-sm btn-info text-white" title="Alterar">
                        <i class="bi bi-pencil"></i>
                    </a>
                    <a href="/odontologia/?delete_odonto={o[0]}" class="btn btn-sm btn-danger" 
                       onclick="return confirm('Excluir este procedimento?')" title="Excluir">
                        <i class="bi bi-trash"></i>
                    </a>
                </div>
            </td>
        </tr>"""

    # 6. HTML da Página
    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center">
            <h4><i class="bi bi-mask"></i> Procedimentos Odontológicos</h4>
            <a href="/admin-painel/" class="btn btn-sm btn-outline-secondary">Voltar ao Dashboard</a>
        </div>
        <hr>
        
        {mensagem}
        
        <form method="POST" class="row g-3 mb-4 bg-light p-3 rounded border shadow-sm">
            <input type="hidden" name="id_odonto" value="{edit_id or ''}">
            
            <div class="col-md-5">
                <label class="form-label fw-bold small">Procedimento</label>
                <input type="text" name="procedimento" class="form-control" value="{o_dados[0]}" placeholder="Ex: Extração de Siso" required>
            </div>
            
            <div class="col-md-4">
                <label class="form-label fw-bold small">Grupo</label>
                <input type="text" name="grupo" class="form-control" value="{o_dados[1]}" placeholder="Ex: Cirurgia, Estética...">
            </div>

            <div class="col-md-3">
                <label class="form-label fw-bold small">Valor Particular (R$)</label>
                <input type="number" step="0.01" name="valor" class="form-control" value="{o_dados[2]}" placeholder="0.00">
            </div>

            <div class="col-12">
                <label class="form-label fw-bold small">Observações Técnicas</label>
                <textarea name="observacoes" class="form-control" rows="2" placeholder="Notas sobre o procedimento...">{o_dados[3]}</textarea>
            </div>

            <div class="col-12">
                <button type="submit" class="btn btn-dark w-100 fw-bold shadow-sm" style="background-color: #555;">
                    { '<i class="bi bi-check-lg"></i> ATUALIZAR PROCEDIMENTO' if edit_id else '<i class="bi bi-plus-lg"></i> SALVAR PROCEDIMENTO' }
                </button>
            </div>
            { f'<div class="col-12 text-center mt-2"><a href="/odontologia/" class="text-danger small text-decoration-none">Cancelar Edição</a></div>' if edit_id else '' }
        </form>

        <hr>
        <h5>Lista de Procedimentos</h5>
        <div class="table-responsive">
            <table class="table table-hover align-middle mt-2">
                <thead class="table-dark">
                    <tr><th>Procedimento / Grupo</th><th>Valor</th><th>Obs.</th><th>Ações</th></tr>
                </thead>
                <tbody>{linhas if lista_odonto else '<tr><td colspan="4" class="text-center text-muted py-4">Nenhum procedimento cadastrado.</td></tr>'}</tbody>
            </table>
        </div>
    """
    return HttpResponse(base_html("Odontologia", conteudo))







# --- 10. TELA 7: GESTÃO DE PACIENTES ---
# --- 10. TELA 7: GESTÃO DE PACIENTES (COM BUSCA E DATA BR) ---
@csrf_exempt
def pacientes_geral(request):
    mensagem = ""
    
    # 1. LÓGICAS DE AÇÃO (BLOQUEIO E EXCLUSÃO)
    if request.GET.get('block_pac'):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE pacientes SET status = 'Bloqueado' WHERE id = %s", [request.GET.get('block_pac')])
        return HttpResponseRedirect('/pacientes/')

    if request.GET.get('delete_pac'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM pacientes WHERE id = %s", [request.GET.get('delete_pac')])
        return HttpResponseRedirect('/pacientes/')

    # 2. CARREGAR DADOS PARA EDIÇÃO
    edit_id = request.GET.get('edit_pac')
    p_dados = ["", "", "Masculino", "", "", "", "", "", "", "", "", "", ""] 
    
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT nome, cpf, sexo, data_nascimento, telefone, convenio_id, cep, 
                       rua, numero, bairro, cidade, estado, observacoes 
                FROM pacientes WHERE id = %s
            """, [edit_id])
            res = cursor.fetchone()
            if res:
                p_dados = list(res)
                if p_dados[3]: p_dados[3] = p_dados[3].strftime('%Y-%m-%d')

    # 3. SALVAR OU ATUALIZAR (POST)
    if request.method == "POST":
        id_post = request.POST.get('id_pac')
        campos = [
            request.POST.get('nome'), request.POST.get('cpf'), request.POST.get('sexo'),
            request.POST.get('data_nasc') or None, request.POST.get('telefone'), 
            request.POST.get('convenio_id') or None, request.POST.get('cep'), 
            request.POST.get('rua'), request.POST.get('numero'), request.POST.get('bairro'), 
            request.POST.get('cidade'), request.POST.get('estado'), request.POST.get('observacoes')
        ]
        
        try:
            with connection.cursor() as cursor:
                if id_post:
                    cursor.execute("""
                        UPDATE pacientes SET 
                            nome=%s, cpf=%s, sexo=%s, data_nascimento=%s, telefone=%s, 
                            convenio_id=%s, cep=%s, rua=%s, numero=%s, bairro=%s, 
                            cidade=%s, estado=%s, observacoes=%s WHERE id=%s
                    """, campos + [id_post])
                else:
                    cursor.execute("""
                        INSERT INTO pacientes 
                        (nome, cpf, sexo, data_nascimento, telefone, convenio_id, cep, rua, numero, bairro, cidade, estado, observacoes) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, campos)
            return HttpResponseRedirect('/pacientes/')
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    # 4. LÓGICA DE PESQUISA (CONVERSÃO DE DATA BR PARA SQL)
    termo_busca = request.GET.get('busca', '')
    termo_sql = termo_busca

    # Se o usuário pesquisar data no formato 10/11/2000, convertemos para 2000-11-10
    if "/" in termo_busca:
        try:
            d, m, a = termo_busca.split('/')
            termo_sql = f"{a}-{m}-{d}"
        except:
            pass # Mantém o original se não conseguir converter

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM convenios ORDER BY nome")
        convenios = cursor.fetchall()
        
        sql_busca = """
            SELECT p.id, p.nome, p.cpf, p.telefone, c.nome, p.status, p.cidade, p.data_nascimento 
            FROM pacientes p 
            LEFT JOIN convenios c ON p.convenio_id = c.id 
        """
        
        params = []
        if termo_busca:
            sql_busca += " WHERE p.cpf LIKE %s OR CAST(p.data_nascimento AS TEXT) LIKE %s OR p.nome ILIKE %s"
            params = [f'%{termo_sql}%', f'%{termo_sql}%', f'%{termo_busca}%']
        
        sql_busca += " ORDER BY p.id DESC"
        cursor.execute(sql_busca, params)
        lista_pacientes = cursor.fetchall()

    # 5. MONTAGEM DO HTML
    opcoes_conv = "".join([f'<option value="{c[0]}" {"selected" if str(c[0])==str(p_dados[5]) else ""}>{c[1]}</option>' for c in convenios])
    
    linhas = ""
    for p in lista_pacientes:
        cor_st = "success" if p[5] == "Ativo" else "danger"
        
        # FORMATAÇÃO DA DATA PARA O PADRÃO BR (10/11/2000)
        data_br = p[7].strftime('%d/%m/%Y') if p[7] else '--'
        
        linhas += f"""
        <tr>
            <td><b>{p[1]}</b><br><small class='text-muted'>CPF: {p[2]} | Nasc: {data_br}</small></td>
            <td>{p[3]}<br><span class="badge bg-{cor_st}">{p[5]}</span></td>
            <td>{p[4] if p[4] else 'Particular'}</td>
            <td>
                <div class="btn-group">
                    <a href="/pacientes/?edit_pac={p[0]}" class="btn btn-sm btn-info text-white" title="Editar"><i class="bi bi-pencil"></i></a>
                    <a href="/pacientes/?block_pac={p[0]}" class="btn btn-sm btn-warning" title="Bloquear"><i class="bi bi-slash-circle"></i></a>
                    <a href="/pacientes/?delete_pac={p[0]}" class="btn btn-sm btn-danger" onclick="return confirm('Excluir?')" title="Excluir"><i class="bi bi-trash"></i></a>
                </div>
            </td>
        </tr>"""

    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4><i class="bi bi-people-fill"></i> Gestão de Pacientes</h4>
            <a href="/admin-painel/" class="btn btn-outline-secondary btn-sm">Painel</a>
        </div>
        
        {mensagem}

        <form method="POST" class="row g-2 mb-4 bg-light p-3 rounded border shadow-sm">
            <input type="hidden" name="id_pac" value="{edit_id or ''}">
            <div class="col-md-5"><label class="small fw-bold">Nome Completo</label><input type="text" name="nome" class="form-control" value="{p_dados[0]}" required></div>
            <div class="col-md-3"><label class="small fw-bold">CPF</label><input type="text" name="cpf" class="form-control" value="{p_dados[1]}"></div>
            <div class="col-md-2"><label class="small fw-bold">Sexo</label><select name="sexo" class="form-select"><option value="Masculino" {"selected" if p_dados[2]=="Masculino" else ""}>M</option><option value="Feminino" {"selected" if p_dados[2]=="Feminino" else ""}>F</option></select></div>
            <div class="col-md-2"><label class="small fw-bold text-danger">Nascimento*</label><input type="date" name="data_nasc" class="form-control" value="{p_dados[3]}" required></div>
            <div class="col-md-4"><label class="small fw-bold text-danger">Telefone*</label><input type="text" name="telefone" class="form-control" value="{p_dados[4]}" required></div>
            <div class="col-md-4"><label class="small fw-bold">Convênio</label><select name="convenio_id" class="form-select"><option value="">Particular</option>{opcoes_conv}</select></div>
            <div class="col-md-4"><label class="small fw-bold">CEP</label><input type="text" name="cep" class="form-control" value="{p_dados[6]}"></div>
            <div class="col-md-5"><label class="small fw-bold">Rua</label><input type="text" name="rua" class="form-control" value="{p_dados[7]}"></div>
            <div class="col-md-2"><label class="small fw-bold">Nº</label><input type="text" name="numero" class="form-control" value="{p_dados[8]}"></div>
            <div class="col-md-5"><label class="small fw-bold">Bairro</label><input type="text" name="bairro" class="form-control" value="{p_dados[9]}"></div>
            <div class="col-md-4"><label class="small fw-bold">Cidade</label><input type="text" name="cidade" class="form-control" value="{p_dados[10]}"></div>
            <div class="col-md-2"><label class="small fw-bold">UF</label><input type="text" name="estado" class="form-control" value="{p_dados[11]}" maxlength="2"></div>
            <div class="col-md-6"><label class="small fw-bold">Observações</label><input type="text" name="observacoes" class="form-control" value="{p_dados[12]}"></div>
            <div class="col-12 mt-3">
                <button type="submit" class="btn btn-danger w-100 fw-bold shadow">
                    {'ATUALIZAR DADOS' if edit_id else 'SALVAR NOVO PACIENTE'}
                </button>
            </div>
            { f'<div class="col-12 text-center mt-2"><a href="/pacientes/" class="text-secondary small">Cancelar Edição</a></div>' if edit_id else '' }
        </form>

        <div class="card mb-3 border-primary shadow-sm">
            <div class="card-body bg-white p-2">
                <form method="GET" class="row g-2">
                    <div class="col-md-10">
                        <input type="text" name="busca" class="form-control" value="{termo_busca}" placeholder="Busque por Nome, CPF ou Data (Ex: 10/11/2000)">
                    </div>
                    <div class="col-md-2">
                        <button type="submit" class="btn btn-primary w-100"><i class="bi bi-search"></i> Pesquisar</button>
                    </div>
                </form>
            </div>
        </div>

        <div class="table-responsive bg-white p-2 rounded shadow-sm border">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-dark">
                    <tr><th>Paciente / Documento</th><th>Contato / Status</th><th>Convênio</th><th>Ações</th></tr>
                </thead>
                <tbody>{linhas if lista_pacientes else f'<tr><td colspan="4" class="text-center py-4 text-muted">Nenhum resultado encontrado para "{termo_busca}"</td></tr>'}</tbody>
            </table>
        </div>
    """
    return HttpResponse(base_html("Pacientes", conteudo))




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
# --- 12. TELA 9: PREÇOS E GRUPOS (CADASTRO EM LOTE COM BOTÃO ALTERAR) ---
@csrf_exempt
def precos_geral(request):
    mensagem = ""
    
    # 1. AÇÃO: EXCLUSÃO
    if request.GET.get('delete_preco'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM precos_convenio WHERE id = %s", [request.GET.get('delete_preco')])
        return HttpResponseRedirect('/precos/')

    # 2. CARREGAR DADOS PARA EDIÇÃO (ALTERAR)
    edit_id = request.GET.get('edit_preco')
    # Ordem: conv_id, esp_id, valor, tipo, grupo
    p_pre = ["", "", 0.00, "A Vista", ""]
    
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT convenio_id, especialidade_id, valor_pagamento, tipo_cobranca, grupo_nome 
                FROM precos_convenio WHERE id = %s
            """, [edit_id])
            res = cursor.fetchone()
            if res:
                p_pre = res

    # 3. SALVAR EM LOTE OU ATUALIZAR (POST)
    if request.method == "POST":
        id_post = request.POST.get('id_preco')
        conv_id = request.POST.get('convenio_id') or None
        tipo = request.POST.get('tipo_cobranca')
        grupo = request.POST.get('grupo_nome')
        
        # Se for uma atualização pontual (via botão alterar)
        if id_post:
            valor_unico = request.POST.get('valor_y') # Usa o campo 'Geral' como valor único na edição
            esp_id = request.POST.get('especialidade_unica') or None
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE precos_convenio SET 
                        convenio_id=%s, valor_pagamento=%s, tipo_cobranca=%s, grupo_nome=%s
                        WHERE id=%s
                    """, [conv_id, valor_unico, tipo, grupo, id_post])
                return HttpResponseRedirect('/precos/')
            except Exception as e:
                mensagem = f'<div class="alert alert-danger">❌ Erro ao atualizar: {e}</div>'
        
        # Se for o cadastro em LOTE (Com Checkboxes)
        else:
            valor_marcadas = request.POST.get('valor_x') 
            valor_outras = request.POST.get('valor_y')   
            selecionadas = request.POST.getlist('especialidades_check')
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM especialidades")
                    todas_especs = [str(row[0]) for row in cursor.fetchall()]

                    for esp_id in todas_especs:
                        valor_final = valor_marcadas if esp_id in selecionadas else valor_outras
                        cursor.execute("""
                            DELETE FROM precos_convenio 
                            WHERE convenio_id=%s AND especialidade_id=%s AND tipo_cobranca=%s
                        """, [conv_id, esp_id, tipo])
                        cursor.execute("""
                            INSERT INTO precos_convenio (convenio_id, especialidade_id, valor_pagamento, tipo_cobranca, grupo_nome) 
                            VALUES (%s, %s, %s, %s, %s)
                        """, [conv_id, esp_id, valor_final, tipo, grupo])
                return HttpResponseRedirect('/precos/')
            except Exception as e:
                mensagem = f'<div class="alert alert-danger">❌ Erro no processamento: {e}</div>'

    # 4. BUSCA DE DADOS
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM convenios ORDER BY nome")
        lista_conv = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM especialidades ORDER BY nome")
        lista_esp = cursor.fetchall()
        cursor.execute("""
            SELECT pr.id, c.nome, e.nome, pr.valor_pagamento, pr.tipo_cobranca, pr.grupo_nome, pr.especialidade_id
            FROM precos_convenio pr
            LEFT JOIN convenios c ON pr.convenio_id = c.id
            LEFT JOIN especialidades e ON pr.especialidade_id = e.id
            ORDER BY pr.grupo_nome, c.nome, e.nome
        """)
        tabela_precos = cursor.fetchall()

    opts_conv = "".join([f'<option value="{c[0]}" {"selected" if str(c[0])==str(p_pre[0]) else ""}>{c[1]}</option>' for c in lista_conv])

    # Checkboxes (Escondidos em modo edição individual para não confundir)
    check_html = ""
    if not edit_id:
        for e in lista_esp:
            check_html += f"""
            <div class="col-md-3 mb-2">
                <div class="form-check form-switch border p-2 rounded bg-white shadow-sm" style="margin-left: 10px;">
                    <input class="form-check-input" type="checkbox" name="especialidades_check" value="{e[0]}" id="esp_{e[0]}">
                    <label class="form-check-label small fw-bold" for="esp_{e[0]}">{e[1]}</label>
                </div>
            </div>"""

    # 5. MONTAGEM DA LISTAGEM COM BOTÃO ALTERAR
    linhas = ""
    for p in tabela_precos:
        badge = "success" if p[4] == "A Vista" else "primary"
        linhas += f"""
        <tr>
            <td><span class="badge bg-{badge}">{p[4]}</span><br><small class="text-muted">{p[5] if p[5] else '---'}</small></td>
            <td><b>{p[1] if p[1] else '---'}</b></td>
            <td>{p[2]}</td>
            <td class="fw-bold text-success">R$ {p[3]}</td>
            <td>
                <div class="btn-group shadow-sm">
                    <a href="/precos/?edit_preco={p[0]}" class="btn btn-sm btn-info text-white" title="Alterar">
                        <i class="bi bi-pencil"></i>
                    </a>
                    <a href="/precos/?delete_preco={p[0]}" class="btn btn-sm btn-danger" onclick="return confirm('Excluir?')" title="Apagar">
                        <i class="bi bi-trash"></i>
                    </a>
                </div>
            </td>
        </tr>"""

    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4><i class="bi bi-tags-fill text-primary"></i> {"Editar Preço Individual" if edit_id else "Configuração de Preços em Lote"}</h4>
            <a href="/admin-painel/" class="btn btn-outline-secondary btn-sm">Voltar</a>
        </div>
        
        {mensagem}

        <form method="POST" class="bg-light p-4 rounded border shadow-sm mb-4">
            <input type="hidden" name="id_preco" value="{edit_id or ''}">
            <input type="hidden" name="especialidade_unica" value="{p_pre[1] if edit_id else ''}">
            
            <div class="row g-3">
                <div class="col-md-4">
                    <label class="fw-bold small">1. Convênio</label>
                    <select name="convenio_id" class="form-select border-primary" required>
                        <option value="">-- Escolha o Convênio --</option>
                        {opts_conv}
                    </select>
                </div>
                <div class="col-md-4">
                    <label class="fw-bold small">2. Cobrança / Grupo</label>
                    <div class="input-group">
                        <select name="tipo_cobranca" class="form-select">
                            <option value="A Vista" {"selected" if p_pre[3]=="A Vista" else ""}>A Vista</option>
                            <option value="Faturado" {"selected" if p_pre[3]=="Faturado" else ""}>Faturado</option>
                        </select>
                        <input type="text" name="grupo_nome" class="form-control" value="{p_pre[4]}" placeholder="Ex: A VISTA 1" required>
                    </div>
                </div>
                
                <div class="col-md-2" {'style="display:none"' if edit_id else ''}>
                    <label class="fw-bold small text-danger">Valor X (Marcadas)</label>
                    <input type="number" step="0.01" name="valor_x" class="form-control fw-bold border-danger" placeholder="Exceção">
                </div>
                <div class="col-md-2">
                    <label class="fw-bold small text-success">{"Valor" if edit_id else "Valor Y (Geral)"}</label>
                    <input type="number" step="0.01" name="valor_y" class="form-control fw-bold border-success" value="{p_pre[2]}" required>
                </div>

                {f'<div class="col-12 mt-4"><label class="fw-bold border-bottom w-100 mb-3 pb-1"><i class="bi bi-check2-square"></i> Marque as Especialidades (Valor X):</label><div class="row">{check_html}</div></div>' if not edit_id else ''}

                <div class="col-12 mt-3">
                    <button type="submit" class="btn btn-primary w-100 fw-bold py-2 shadow">
                        { '<i class="bi bi-check-lg"></i> ATUALIZAR ESTE REGISTRO' if edit_id else '<i class="bi bi-lightning-fill"></i> GERAR TABELA EM LOTE' }
                    </button>
                </div>
            </div>
            { f'<div class="col-12 text-center mt-2"><a href="/precos/" class="text-danger small">Cancelar Edição</a></div>' if edit_id else '' }
        </form>

        <div class="table-responsive bg-white p-2 rounded shadow-sm border">
            <table class="table table-hover table-sm align-middle mb-0">
                <thead class="table-dark">
                    <tr><th>Tipo/Grupo</th><th>Convênio</th><th>Especialidade</th><th>Valor</th><th>Ações</th></tr>
                </thead>
                <tbody>{linhas if tabela_precos else '<tr><td colspan="5" class="text-center py-4">Nenhum preço configurado.</td></tr>'}</tbody>
            </table>
        </div>
    """
    return HttpResponse(base_html("Tabela de Preços", conteudo))





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
# --- 14. TELA 11: CONFIGURAÇÃO DE AGENDAS (COM TRAVA DE UNIDADE) ---
@csrf_exempt
def agendas_config_geral(request):
    mensagem = ""
    
    # 1. AÇÕES: EXCLUSÃO
    if request.GET.get('delete_agenda'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM agendas_config WHERE id = %s", [request.GET.get('delete_agenda')])
        return HttpResponseRedirect('/agendas-config/')

    # 2. CARREGAR DADOS PARA EDIÇÃO
    edit_id = request.GET.get('edit_agenda')
    a_dados = ["", "", "", "", "", 20] # unid, prof, data, inicio, fim, inter
    
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT unidade_id, profissional_id, data_especifica, 
                       horario_inicio, horario_fim, intervalo_minutos 
                FROM agendas_config WHERE id = %s
            """, [edit_id])
            res = cursor.fetchone()
            if res:
                a_dados = list(res)
                if a_dados[2]: a_dados[2] = a_dados[2].strftime('%Y-%m-%d')

    # 3. SALVAR / ATUALIZAR (POST)
    if request.method == "POST":
        id_post = request.POST.get('id_agenda')
        unid = request.POST.get('unidade_id')
        prof = request.POST.get('profissional_id')
        data_ag = request.POST.get('data_ag') or None
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')
        inter = request.POST.get('intervalo') or 20

        try:
            with connection.cursor() as cursor:
                if id_post:
                    cursor.execute("""
                        UPDATE agendas_config SET 
                        unidade_id=%s, profissional_id=%s, data_especifica=%s, 
                        horario_inicio=%s, horario_fim=%s, intervalo_minutos=%s
                        WHERE id=%s
                    """, [unid, prof, data_ag, inicio, fim, inter, id_post])
                else:
                    cursor.execute("""
                        INSERT INTO agendas_config 
                        (unidade_id, profissional_id, data_especifica, horario_inicio, horario_fim, intervalo_minutos) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, [unid, prof, data_ag, inicio, fim, inter])
            return HttpResponseRedirect('/agendas-config/')
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    # 4. BUSCA DE DADOS
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()
        
        # Puxamos profissionais COM o ID da unidade vinculada para o JavaScript filtrar
        cursor.execute("""
            SELECT p.id, p.nome, e.nome, p.unidade_id 
            FROM profissionais p 
            LEFT JOIN especialidades e ON p.especialidade_id = e.id 
            ORDER BY p.nome
        """)
        profs = cursor.fetchall()
        
        cursor.execute("""
            SELECT ac.id, u.nome, p.nome, ac.data_especifica, 
                   ac.horario_inicio, ac.horario_fim, e.nome, ac.intervalo_minutos
            FROM agendas_config ac
            JOIN unidades u ON ac.unidade_id = u.id
            JOIN profissionais p ON ac.profissional_id = p.id
            LEFT JOIN especialidades e ON p.especialidade_id = e.id
            ORDER BY u.nome ASC, ac.data_especifica ASC
        """)
        lista_agendas = cursor.fetchall()

    # 5. MONTAGEM DO HTML
    opts_unid = "".join([f'<option value="{u[0]}" {"selected" if str(u[0])==str(a_dados[0]) else ""}>{u[1]}</option>' for u in unidades])
    
    # Criamos um "dicionário" em JavaScript para o filtro dinâmico
    linhas_tabela = ""
    for a in lista_agendas:
        data_f = a[3].strftime('%d/%m/%Y') if a[3] else "--"
        linhas_tabela += f"""
            <tr>
                <td><span class="badge bg-primary">{a[1]}</span></td>
                <td><b>{a[2]}</b><br><small>{a[6] if a[6] else ''}</small></td>
                <td>{data_f} <br> <small class="text-muted">{a[4]} - {a[5]}</small></td>
                <td>{a[7]} min</td>
                <td>
                    <a href="/agendas-config/?edit_agenda={a[0]}" class="btn btn-sm btn-info text-white"><i class="bi bi-pencil"></i></a>
                    <a href="/agendas-config/?delete_agenda={a[0]}" class="btn btn-sm btn-danger"><i class="bi bi-trash"></i></a>
                </td>
            </tr>"""

    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4><i class="bi bi-calendar-range text-primary"></i> Configuração de Grades</h4>
            <a href="/admin-painel/" class="btn btn-sm btn-outline-secondary">Voltar</a>
        </div>
        
        {mensagem}

        <form method="POST" id="formAgenda" class="card p-3 shadow-sm bg-light border-primary mb-4">
            <input type="hidden" name="id_agenda" value="{edit_id or ''}">
            <div class="row g-3">
                
                <div class="col-md-4">
                    <label class="fw-bold small text-primary">1º Escolha a Unidade</label>
                    <select name="unidade_id" id="select_unidade" class="form-select border-primary" onchange="filtrarProfissionais()" required>
                        <option value="">-- Selecione a Unidade --</option>
                        {opts_unid}
                    </select>
                </div>

                <div class="col-md-5">
                    <label class="fw-bold small text-primary">2º Profissional Disponível</label>
                    <select name="profissional_id" id="select_profissional" class="form-select border-primary" required disabled>
                        <option value="">-- Selecione a Unidade Antes --</option>
                    </select>
                </div>

                <div class="col-md-3">
                    <label class="fw-bold small">Data da Agenda</label>
                    <input type="date" name="data_ag" class="form-control" value="{a_dados[2]}" required>
                </div>

                <div class="col-md-4">
                    <label class="fw-bold small">Início</label>
                    <input type="time" name="inicio" class="form-control" value="{a_dados[3]}" required>
                </div>
                <div class="col-md-4">
                    <label class="fw-bold small">Fim</label>
                    <input type="time" name="fim" class="form-control" value="{a_dados[4]}" required>
                </div>
                <div class="col-md-4">
                    <label class="fw-bold small">Intervalo (Min)</label>
                    <input type="number" name="intervalo" class="form-control" value="{a_dados[5]}" required>
                </div>

                <div class="col-12 mt-3">
                    <button type="submit" class="btn btn-primary w-100 fw-bold shadow">
                        { '<i class="bi bi-arrow-repeat"></i> ATUALIZAR GRADE' if edit_id else '<i class="bi bi-plus-lg"></i> GERAR GRADE' }
                    </button>
                </div>
                { f'<div class="col-12 text-center mt-2"><a href="/agendas-config/" class="text-danger small">Cancelar Edição</a></div>' if edit_id else '' }
            </div>
        </form>

        <script>
            // Dados dos profissionais injetados pelo Python para o JS
            const profissionais = [
                { "".join([f'{{id: {p[0]}, nome: "{p[1]} ({p[2]})", unidade: "{p[3]}"}},' for p in profs]) }
            ];

            function filtrarProfissionais() {{
                const unidId = document.getElementById('select_unidade').value;
                const selectProf = document.getElementById('select_profissional');
                
                selectProf.innerHTML = '<option value="">-- Selecione o Profissional --</option>';
                
                if (unidId === "") {{
                    selectProf.disabled = true;
                    return;
                }}

                const filtrados = profissionais.filter(p => p.unidade == unidId);

                if (filtrados.length > 0) {{
                    filtrados.forEach(p => {{
                        const opt = document.createElement('option');
                        opt.value = p.id;
                        opt.text = p.nome;
                        // Se estiver editando, pré-seleciona
                        if(p.id == "{a_dados[1]}") opt.selected = true;
                        selectProf.appendChild(opt);
                    }});
                    selectProf.disabled = false;
                }} else {{
                    selectProf.innerHTML = '<option value="">Nenhum médico cadastrado nesta unidade</option>';
                    selectProf.disabled = true;
                }}
            }}

            // Executa ao carregar caso seja modo edição
            window.onload = filtrarProfissionais;
        </script>

        <div class="table-responsive bg-white rounded shadow-sm border">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-dark">
                    <tr><th>Unidade</th><th>Profissional</th><th>Data/Hora</th><th>Intervalo</th><th>Ações</th></tr>
                </thead>
                <tbody>{linhas_tabela if lista_agendas else '<tr><td colspan="5" class="text-center py-4">Nenhuma grade encontrada.</td></tr>'}</tbody>
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
# --- TELA 13: AGENDAMENTO (VERSÃO FINAL COM FILTROS E GRADE) ---
@csrf_exempt
def agendar_consulta(request):
    mensagem = ""
    hoje = datetime.date.today()

    # Captura de filtros
    unid_id = request.GET.get('unidade_id')
    esp_id = request.GET.get('especialidade_id')
    prof_id = request.GET.get('profissional_id')
    data_sel = request.GET.get('data_sel') # Data da consulta
    hora_sel = request.GET.get('hora_sel') # Horário escolhido

    with connection.cursor() as cursor:
        # 1. Busca Unidades e Especialidades para os filtros iniciais
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM especialidades ORDER BY nome")
        especialidades = cursor.fetchall()

        # 2. Busca Médicos que possuem grade configurada para a unidade/especialidade
        profs_filtrados = []
        if unid_id and esp_id:
            cursor.execute("""
                SELECT DISTINCT p.id, p.nome 
                FROM profissionais p
                JOIN agendas_config ac ON p.id = ac.profissional_id
                WHERE ac.unidade_id = %s AND ac.especialidade_id = %s
            """, [unid_id, esp_id])
            profs_filtrados = cursor.fetchall()

        # 3. GERAÇÃO DA GRADE DE HORÁRIOS (Se médico e data forem selecionados)
        horarios_disponiveis = []
        if prof_id and data_sel:
            cursor.execute("""
                SELECT horario_inicio, horario_fim, intervalo_minutos, id 
                FROM agendas_config 
                WHERE profissional_id = %s AND data_especifica = %s AND unidade_id = %s
            """, [prof_id, data_sel, unid_id])
            grade = cursor.fetchone()
            
            if grade:
                inicio = datetime.datetime.combine(hoje, grade[0])
                fim = datetime.datetime.combine(hoje, grade[1])
                intervalo = datetime.timedelta(minutes=grade[2])
                
                # Buscar horários já ocupados
                cursor.execute("SELECT horario_selecionado FROM agendamentos WHERE agenda_config_id = %s AND data_agendamento = %s", [grade[3], data_sel])
                ocupados = [r[0].strftime('%H:%M') for r in cursor.fetchall()]

                atual = inicio
                while atual < fim:
                    h_str = atual.strftime('%H:%M')
                    if h_str not in ocupados:
                        horarios_disponiveis.append(h_str)
                    atual += intervalo

        # 4. Busca Convênios para o formulário final
        cursor.execute("SELECT id, nome FROM convenios ORDER BY nome")
        convenios = cursor.fetchall()

    # 5. SALVAR AGENDAMENTO (POST)
    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        whatsapp = request.POST.get('whatsapp')
        conv_id = request.POST.get('convenio')
        
        try:
            with connection.cursor() as cursor:
                # Cria ou recupera paciente pelo WhatsApp (Evita duplicar)
                cursor.execute("INSERT INTO pacientes (nome, telefone, convenio_id) VALUES (%s, %s, %s) RETURNING id", 
                               [f"{nome} {sobrenome}", whatsapp, conv_id if conv_id else None])
                paciente_id = cursor.fetchone()[0]

                # Registra a consulta
                cursor.execute("""
                    INSERT INTO agendamentos (paciente_id, agenda_config_id, data_agendamento, horario_selecionado, status)
                    VALUES (%s, (SELECT id FROM agendas_config WHERE profissional_id=%s AND data_especifica=%s LIMIT 1), %s, %s, 'Agendado')
                """, [paciente_id, prof_id, data_sel, data_sel, hora_sel])
                
            mensagem = f"<div class='alert alert-success'>✅ Pronto! Consulta agendada para {data_sel} às {hora_sel}</div>"
        except Exception as e:
            mensagem = f"<div class='alert alert-danger'>❌ Erro ao agendar: {e}</div>"

    # MONTAGEM DO HTML
    opts_unid = "".join([f'<option value="{u[0]}" {"selected" if str(u[0])==unid_id else ""}>{u[1]}</option>' for u in unidades])
    opts_esp = "".join([f'<option value="{e[0]}" {"selected" if str(e[0])==esp_id else ""}>{e[1]}</option>' for e in especialidades])
    opts_prof = "".join([f'<option value="{p[0]}" {"selected" if str(p[0])==prof_id else ""}>{p[1]}</option>' for p in profs_filtrados])
    opts_conv = "".join([f'<option value="{c[0]}">{c[1]}</option>' for c in convenios])

    btns_horas = "".join([f'<a href="?unidade_id={unid_id}&especialidade_id={esp_id}&profissional_id={prof_id}&data_sel={data_sel}&hora_sel={h}" class="btn btn-outline-primary btn-sm m-1 {"active" if h==hora_sel else ""}">{h}</a>' for h in horarios_disponiveis])

    conteudo = f"""
        <div class="container py-3">
            <h4 class="text-center mb-4"><i class="bi bi-calendar-check"></i> Agendamento Online</h4>
            {mensagem}

            <div class="card p-3 shadow-sm mb-4 border-primary">
                <form method="GET" class="row g-2">
                    <div class="col-md-4">
                        <label class="small fw-bold">Unidade</label>
                        <select name="unidade_id" class="form-select" onchange="this.form.submit()"><option value="">Selecione...</option>{opts_unid}</select>
                    </div>
                    <div class="col-md-4">
                        <label class="small fw-bold">Especialidade</label>
                        <select name="especialidade_id" class="form-select" onchange="this.form.submit()"><option value="">Selecione...</option>{opts_esp}</select>
                    </div>
                    <div class="col-md-4">
                        <label class="small fw-bold">Médico</label>
                        <select name="profissional_id" class="form-select" onchange="this.form.submit()"><option value="">Selecione...</option>{opts_prof}</select>
                    </div>
                </form>
            </div>

            {f'''
            <div class="card p-3 shadow-sm mb-4">
                <h6 class="fw-bold"><i class="bi bi-clock"></i> Escolha a Data e o Horário</h6>
                <form method="GET" class="mb-3">
                    <input type="hidden" name="unidade_id" value="{unid_id}"><input type="hidden" name="especialidade_id" value="{esp_id}"><input type="hidden" name="profissional_id" value="{prof_id}">
                    <input type="date" name="data_sel" class="form-control" value="{data_sel}" onchange="this.form.submit()">
                </form>
                <div class="d-flex flex-wrap justify-content-center">{btns_horas if btns_horas else '<small class="text-muted">Nenhum horário disponível para esta data.</small>'}</div>
            </div>
            ''' if prof_id else ""}

            {f'''
            <div class="card p-4 shadow-sm border-success">
                <h6 class="fw-bold text-success border-bottom pb-2">Finalizar Agendamento: {data_sel} às {hora_sel}</h6>
                <form method="POST" class="row g-3 mt-1">
                    <input type="hidden" name="hora_sel" value="{hora_sel}">
                    <div class="col-md-6"><label class="small">Nome</label><input type="text" name="nome" class="form-control" required></div>
                    <div class="col-md-6"><label class="small">Sobrenome</label><input type="text" name="sobrenome" class="form-control" required></div>
                    <div class="col-md-6"><label class="small">WhatsApp</label><input type="text" name="whatsapp" class="form-control" placeholder="(00) 00000-0000" required></div>
                    <div class="col-md-6">
                        <label class="small">Convênio</label>
                        <select name="convenio" class="form-select"><option value="">Particular</option>{opts_conv}</select>
                    </div>
                    <div class="col-12 mt-4">
                        <button class="btn btn-success w-100 fw-bold py-2">CONFIRMAR AGENDAMENTO</button>
                    </div>
                </form>
            </div>
            ''' if hora_sel else ""}
        </div>
    """
    return HttpResponse(base_html("Agendar", conteudo))





# --- TELA 14 FINAL: RECEPÇÃO INTEGRADA ---
# --- TELA 14: RECEPÇÃO INTEGRADA (VERSÃO FINAL) ---
@csrf_exempt
def recepcao_geral(request):
    data_hoje = datetime.date.today()
    unidade_filtro = request.GET.get('unidade')
    mensagem = ""

    with connection.cursor() as cursor:
        # 1. BUSCA UNIDADES PARA O FILTRO
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()

        # 2. LÓGICA DE AÇÕES (CHEGADA / FINALIZAR)
        if request.GET.get('acao'):
            ag_id = request.GET.get('id')
            novo_status = {"chegada": "Aguardando", "finalizar": "Finalizado"}.get(request.GET.get('acao'), "Aguardando")
            cursor.execute("UPDATE agendamentos SET status = %s WHERE id = %s", [novo_status, ag_id])
            return HttpResponseRedirect(f'/recepcao/?unidade={unidade_filtro or ""}')

        # 3. BUSCA GRADES ABERTAS HOJE (PARA VER DISPONIBILIDADE)
        sql_grades = """
            SELECT u.nome, e.nome, p.nome, ac.horario_inicio, ac.horario_fim, ac.id
            FROM agendas_config ac
            JOIN unidades u ON ac.unidade_id = u.id
            JOIN profissionais p ON ac.profissional_id = p.id
            LEFT JOIN especialidades e ON p.especialidade_id = e.id
            WHERE ac.data_especifica = %s
        """
        params_g = [data_hoje]
        if unidade_filtro:
            sql_grades += " AND u.id = %s"
            params_g.append(unidade_filtro)
        
        cursor.execute(sql_grades + " ORDER BY u.nome, p.nome", params_g)
        grades_hoje = cursor.fetchall()

        # 4. BUSCAR AGENDAMENTOS DO DIA
        sql_ag = """
            SELECT ag.id, pac.nome, prof.nome, u.nome, ag.horario_selecionado, ag.status, esp.nome
            FROM agendamentos ag
            JOIN pacientes pac ON ag.paciente_id = pac.id
            JOIN agendas_config ac ON ag.agenda_config_id = ac.id
            JOIN profissionais prof ON ac.profissional_id = prof.id
            JOIN unidades u ON ac.unidade_id = u.id
            LEFT JOIN especialidades esp ON prof.especialidade_id = esp.id
            WHERE ag.data_agendamento = %s
        """
        params_ag = [data_hoje]
        if unidade_filtro:
            sql_ag += " AND u.id = %s"
            params_ag.append(unidade_filtro)
            
        cursor.execute(sql_ag + " ORDER BY ag.horario_selecionado", params_ag)
        agenda = cursor.fetchall()

    # MONTAGEM DO HTML - GRADES DISPONÍVEIS (CARDS)
    cards_disponibilidade = ""
    for g in grades_hoje:
        cards_disponibilidade += f"""
        <div class="col-md-4 mb-3">
            <div class="card border-left-primary shadow h-100 py-2 bg-light">
                <div class="card-body p-2">
                    <div class="small fw-bold text-primary text-uppercase mb-1">{g[1]} (Especialidade)</div>
                    <div class="h6 mb-0 fw-bold text-gray-800">{g[2]} (Médico)</div>
                    <div class="text-xs text-muted">Grade: {g[3]} às {g[4]} | Unid: {g[0]}</div>
                </div>
            </div>
        </div>"""

    # MONTAGEM DA TABELA DE PACIENTES
    linhas_pacientes = ""
    for a in agenda:
        hora = a[4].strftime('%H:%M') if not isinstance(a[4], str) else a[4][:5]
        status = a[5] or "Agendado"
        cor = {"Aguardando": "warning", "Em Atendimento": "primary", "Finalizado": "success", "Agendado": "info"}.get(status, "secondary")
        
        linhas_pacientes += f"""
            <tr>
                <td><b class="text-dark">{hora}</b></td>
                <td>{a[1]}<br><small class="text-muted">{a[6]}</small></td>
                <td>{a[2]}</td>
                <td><span class="badge bg-{cor}">{status}</span></td>
                <td>
                    <div class="btn-group">
                        <a href="/recepcao/?acao=chegada&id={a[0]}&unidade={unidade_filtro or ''}" class="btn btn-sm btn-warning" title="Chegada"><i class="bi bi-person-down"></i></a>
                        <a href="/prontuario/?id={a[0]}" class="btn btn-sm btn-primary" title="Atender"><i class="bi bi-Stethoscope"></i></a>
                        <a href="/recepcao/?acao=finalizar&id={a[0]}&unidade={unidade_filtro or ''}" class="btn btn-sm btn-success" title="Finalizar"><i class="bi bi-check-all"></i></a>
                    </div>
                </td>
            </tr>"""

    opts_unidades = "".join([f'<option value="{u[0]}" {"selected" if str(u[0])==str(unidade_filtro) else ""}>{u[1]}</option>' for u in unidades])

    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4><i class="bi bi-display text-primary"></i> Painel da Recepção - {data_hoje.strftime('%d/%m/%Y')}</h4>
            <a href="/admin-painel/" class="btn btn-outline-secondary btn-sm">Dashboard</a>
        </div>

        <div class="card mb-4 shadow-sm border-0 bg-dark text-white">
            <div class="card-body p-2">
                <form method="GET" class="row g-2 align-items-center">
                    <div class="col-md-4"><select name="unidade" class="form-select form-select-sm">{f'<option value="">Todas as Unidades</option>'}{opts_unidades}</select></div>
                    <div class="col-md-2"><button class="btn btn-sm btn-primary w-100 fw-bold">FILTRAR PAINEL</button></div>
                </form>
            </div>
        </div>

        <h6 class="fw-bold mb-3"><i class="bi bi-calendar-check"></i> Médicos com Grade Aberta Hoje</h6>
        <div class="row mb-4">{cards_disponibilidade if grades_hoje else '<div class="col-12 text-muted small">Nenhuma grade aberta para hoje nesta unidade.</div>'}</div>

        <h6 class="fw-bold mb-3"><i class="bi bi-people"></i> Lista de Atendimentos</h6>
        <div class="table-responsive bg-white rounded shadow-sm border">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                    <tr><th>Horário</th><th>Paciente / Especialidade</th><th>Médico</th><th>Status</th><th>Ações</th></tr>
                </thead>
                <tbody>{linhas_pacientes if agenda else '<tr><td colspan="5" class="text-center py-4 text-muted">Nenhum paciente agendado para hoje.</td></tr>'}</tbody>
            </table>
        </div>
    """
    return HttpResponse(base_html("Recepção", conteudo))






# --- TELA 15: PRONTUÁRIO ---
@csrf_exempt
def prontuario_geral(request):

    agendamento_id = request.GET.get('id')
    mensagem = ""

    try:
        with connection.cursor() as cursor:

            # 🔹 Buscar dados do agendamento
            cursor.execute("""
                SELECT 
                    p.id,
                    p.nome,
                    p.telefone,
                    c.nome,
                    pr.id,
                    pr.nome,
                    ag.data_agendamento,
                    ag.horario_selecionado
                FROM agendamentos ag
                JOIN pacientes p ON ag.paciente_id = p.id
                LEFT JOIN convenios c ON p.convenio_id = c.id
                JOIN agendas_config ac ON ag.agenda_config_id = ac.id
                JOIN profissionais pr ON ac.profissional_id = pr.id
                WHERE ag.id = %s
            """, [agendamento_id])

            dados = cursor.fetchone()

            if not dados:
                return HttpResponse(base_html("Erro", "Agendamento não encontrado"))

            paciente_id = dados[0]
            paciente_nome = dados[1]
            telefone = dados[2]
            convenio = dados[3] or "Particular"
            profissional_id = dados[4]
            profissional_nome = dados[5]
            data = dados[6]
            hora = dados[7]

            # 🔹 Histórico do paciente
            cursor.execute("""
                SELECT data_atendimento, diagnostico, procedimentos
                FROM prontuarios
                WHERE paciente_id = %s
                ORDER BY data_atendimento DESC
            """, [paciente_id])

            historico = cursor.fetchall()

    except Exception as e:
        return HttpResponse(base_html("Erro", f"<pre>{e}</pre>"))

    # 🔹 SALVAR PRONTUÁRIO
    if request.method == "POST":

        queixa = request.POST.get('queixa')
        anamnese = request.POST.get('anamnese')
        diagnostico = request.POST.get('diagnostico')
        procedimentos = request.POST.get('procedimentos')
        obs = request.POST.get('observacoes')

        try:
            with connection.cursor() as cursor:

                cursor.execute("""
                    INSERT INTO prontuarios 
                    (paciente_id, profissional_id, data_atendimento, hora,
                     queixa, anamnese, diagnostico, procedimentos, observacoes)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, [
                    paciente_id,
                    profissional_id,
                    data,
                    hora,
                    queixa,
                    anamnese,
                    diagnostico,
                    procedimentos,
                    obs
                ])

                # 🔹 finalizar atendimento automaticamente
                cursor.execute("""
                    UPDATE agendamentos
                    SET status = 'Finalizado'
                    WHERE id = %s
                """, [agendamento_id])

            mensagem = "<div class='alert alert-success'>✅ Prontuário salvo!</div>"

        except Exception as e:
            mensagem = f"<div class='alert alert-danger'>❌ Erro: {e}</div>"

    # 🔹 montar histórico
    linhas_hist = ""
    for h in historico:
        linhas_hist += f"""
            <tr>
                <td>{h[0]}</td>
                <td>{h[1]}</td>
                <td>{h[2]}</td>
            </tr>
        """

    conteudo = f"""
        <h4><i class="bi bi-file-medical"></i> Prontuário</h4>
        {mensagem}

        <div class="mb-3">
            <b>Paciente:</b> {paciente_nome} <br>
            <b>Telefone:</b> {telefone} <br>
            <b>Convênio:</b> {convenio} <br><br>

            <b>Profissional:</b> {profissional_nome} <br>
            <b>Data:</b> {data} <br>
            <b>Hora:</b> {hora}
        </div>

        <form method="POST">

            <label>Queixa Principal</label>
            <textarea name="queixa" class="form-control mb-2"></textarea>

            <label>Anamnese</label>
            <textarea name="anamnese" class="form-control mb-2"></textarea>

            <label>Diagnóstico</label>
            <textarea name="diagnostico" class="form-control mb-2"></textarea>

            <label>Procedimentos</label>
            <textarea name="procedimentos" class="form-control mb-2"></textarea>

            <label>Observações</label>
            <textarea name="observacoes" class="form-control mb-3"></textarea>

            <button class="btn btn-success w-100">Salvar Prontuário</button>
        </form>

        <hr>

        <h5>Histórico do Paciente</h5>

        <table class="table table-sm">
            <thead class="table-dark">
                <tr>
                    <th>Data</th>
                    <th>Diagnóstico</th>
                    <th>Procedimentos</th>
                </tr>
            </thead>
            <tbody>
                {linhas_hist if linhas_hist else "<tr><td colspan='3'>Sem histórico</td></tr>"}
            </tbody>
        </table>
    """

    return HttpResponse(base_html("Prontuário", conteudo))


# --_16.TELA ----


@csrf_exempt
def caixa_geral(request):
    mensagem = ""

    try:
        # --- REGISTRAR PAGAMENTO ---
        if request.method == "POST":
            atendimento_id = request.POST.get('atendimento_id')
            valor = request.POST.get('valor')
            forma = request.POST.get('forma_pagamento')

            with connection.cursor() as cursor:
                # Busca dados do atendimento
                cursor.execute("""
                    SELECT p.nome, pr.nome, e.nome
                    FROM agenda_diaria ag
                    LEFT JOIN pacientes p ON ag.paciente_id = p.id
                    LEFT JOIN profissionais pr ON ag.profissional_id = pr.id
                    LEFT JOIN especialidades e ON ag.especialidade_id = e.id
                    WHERE ag.id = %s
                """, [atendimento_id])

                dados = cursor.fetchone()

                if dados:
                    paciente = dados[0] or "Não informado"
                    profissional = dados[1] or "Não informado"
                    especialidade = dados[2] or "Não informado"

                    # Salva no caixa
                    cursor.execute("""
                        INSERT INTO caixa 
                        (atendimento_id, paciente_nome, profissional_nome, especialidade, valor, forma_pagamento, status, data_atendimento)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_DATE)
                    """, [
                        atendimento_id,
                        paciente,
                        profissional,
                        especialidade,
                        valor,
                        forma,
                        'Pago'
                    ])

                    # Atualiza status da agenda
                    cursor.execute("""
                        UPDATE agenda_diaria 
                        SET status = 'Finalizado'
                        WHERE id = %s
                    """, [atendimento_id])

                    mensagem = '<div class="alert alert-success">✅ Pagamento registrado com sucesso!</div>'
                else:
                    mensagem = '<div class="alert alert-danger">❌ Atendimento não encontrado!</div>'

        # --- BUSCAR ATENDIMENTOS PARA COBRANÇA ---
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ag.id, p.nome, pr.nome, e.nome, ag.horario, ag.status
                FROM agenda_diaria ag
                LEFT JOIN pacientes p ON ag.paciente_id = p.id
                LEFT JOIN profissionais pr ON ag.profissional_id = pr.id
                LEFT JOIN especialidades e ON ag.especialidade_id = e.id
                WHERE ag.status IN ('Aguardando Atendimento', 'Atendido')
                ORDER BY ag.horario
            """)
            atendimentos = cursor.fetchall()

        # --- BUSCAR MOVIMENTO DO CAIXA ---
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT paciente_nome, profissional_nome, especialidade, valor, forma_pagamento, data_pagamento
                FROM caixa
                ORDER BY data_pagamento DESC
                LIMIT 20
            """)
            caixa_lista = cursor.fetchall()

    except Exception as e:
        return HttpResponse(base_html("Erro Caixa", f"<h4>Erro:</h4><pre>{e}</pre>"))

    # --- TABELA ATENDIMENTOS ---
    linhas_atend = ""
    for a in atendimentos:
        linhas_atend += f"""
        <tr>
            <td>{a[1] or '---'}</td>
            <td>{a[2] or '---'}</td>
            <td>{a[3] or '---'}</td>
            <td>{a[4]}</td>
            <td>
                <form method="POST" class="d-flex gap-1">
                    <input type="hidden" name="atendimento_id" value="{a[0]}">
                    <input type="number" step="0.01" name="valor" class="form-control form-control-sm" placeholder="Valor" required>
                    <select name="forma_pagamento" class="form-select form-select-sm">
                        <option>Dinheiro</option>
                        <option>Cartão</option>
                        <option>Pix</option>
                        <option>Convênio</option>
                    </select>
                    <button class="btn btn-success btn-sm">Cobrar</button>
                </form>
            </td>
        </tr>
        """

    # --- TABELA CAIXA ---
    linhas_caixa = ""
    for c in caixa_lista:
        linhas_caixa += f"""
        <tr>
            <td>{c[0]}</td>
            <td>{c[1]}</td>
            <td>{c[2]}</td>
            <td>R$ {c[3]}</td>
            <td>{c[4]}</td>
            <td>{c[5]}</td>
        </tr>
        """

    conteudo = f"""
        <h4><i class="bi bi-cash-coin"></i> Caixa</h4>
        {mensagem}

        <h5 class="mt-4">💰 Atendimentos para Cobrança</h5>
        <table class="table table-hover">
            <thead class="table-dark">
                <tr><th>Paciente</th><th>Profissional</th><th>Especialidade</th><th>Horário</th><th>Ação</th></tr>
            </thead>
            <tbody>
                {linhas_atend if linhas_atend else '<tr><td colspan="5" class="text-center">Nenhum atendimento</td></tr>'}
            </tbody>
        </table>

        <h5 class="mt-4">📊 Últimos Recebimentos</h5>
        <table class="table table-striped">
            <thead class="table-dark">
                <tr><th>Paciente</th><th>Profissional</th><th>Especialidade</th><th>Valor</th><th>Forma</th><th>Data</th></tr>
            </thead>
            <tbody>
                {linhas_caixa if linhas_caixa else '<tr><td colspan="6" class="text-center">Sem registros</td></tr>'}
            </tbody>
        </table>
    """

    return HttpResponse(base_html("Caixa", conteudo))








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
    path('prontuario/', prontuario_geral),
    path('caixa/', caixa_geral),
    path('admin-painel/', painel_controle, name='painel'),
   
   
]
