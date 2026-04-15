import datetime, urllib.parse
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import views 
 


# --- 1. TEMPLATE BASE (COMPLETO + USUÁRIO DINÂMICO) ---

def base_html(request, titulo, conteudo):
    # ✅ Lógica para capturar o nome de quem está acessando
    usuario_logado = "Visitante"
    if request.user.is_authenticated:
        usuario_logado = request.user.get_full_name() or request.user.username

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
            <div class="small"><i class="bi bi-person-circle"></i> {usuario_logado}</div>
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
                <li><a href="/logout/" class="text-danger fw-bold"><i class="bi bi-box-arrow-right"></i> Sair do Sistema</a></li>
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













# --- 2. TELA 0: PAINEL DE GESTÃO (VERSÃO PROFISSIONAL CORRIGIDA) ---

def painel_controle(request):
    # Definimos o conteúdo usando o grid system col-md-4 para 3 colunas perfeitas
    conteudo = """
        <div class="mb-4">
            <h3 class="fw-bold text-dark"><i class="bi bi-speedometer2 text-primary"></i> Painel de Gestão</h3>
            <p class="text-muted">Bem-vindo, COLABORADOR. Gerencie as operações da clínica Sempre Vida.</p>
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





# --- 6. TELA 4: CONVÊNIOS ---
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








# --- 7. TELA 5: EXAMES ---
# --- 7. TELA 5: EXAMES + CAIXA EXAMES (COM UNIDADE E AUDITORIA) ---
@login_required  # ✅ OBRIGATÓRIO para o request.user funcionar
@csrf_exempt
def exames_geral(request):
    from django.db import connection
    from django.http import HttpResponse, HttpResponseRedirect
    import datetime

    mensagem = ""
    # ✅ CAPTURA O USUÁRIO LOGADO
    usuario_nome = request.user.username if request.user.is_authenticated else "sistema"

    # ===============================
    # EXCLUIR EXAME
    # ===============================
    if request.GET.get('delete_exame'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM exames WHERE id = %s", [request.GET.get('delete_exame')])
        return HttpResponseRedirect('/exames/')

    # ===============================
    # CADASTRAR PRESTADOR
    # ===============================
    if request.method == "POST" and "novo_prestador" in request.POST:
        try:
            nome = request.POST.get('nome_prestador')
            if nome:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO prestadores (nome) VALUES (%s)", [nome])
                mensagem = '<div class="alert alert-success">✅ Prestador cadastrado!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ {e}</div>'

    # ===============================
    # LANÇAMENTO CAIXA EXAMES (COM AUDITORIA)
    # ===============================
    if request.method == "POST" and "lancar_exame" in request.POST:
        try:
            paciente = request.POST.get('paciente')
            exame_id = request.POST.get('exame_id')
            prestador = request.POST.get('prestador')
            valor = float(request.POST.get('valor') or 0)
            forma = request.POST.get('forma')
            unidade_id = request.POST.get('unidade_id')

            if not paciente or not exame_id:
                raise Exception("Paciente e exame obrigatórios")
            if not unidade_id:
                raise Exception("Selecione a unidade")

            with connection.cursor() as cursor:
                cursor.execute("SELECT nome FROM exames WHERE id = %s", [exame_id])
                ex = cursor.fetchone()
                nome_exame = ex[0] if ex else "Exame"

                # ✅ SQL CORRIGIDO PARA A TABELA CAIXA (10 colunas)
                cursor.execute("""
                    INSERT INTO caixa
                    (paciente_nome, profissional_nome, valor, forma_pagamento, status, 
                     categoria, descricao, data_pagamento, unidade_id, usuario_lancamento)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE,%s,%s)
                """, [paciente, prestador, valor, forma, 'Pago', 'Exame', nome_exame, unidade_id, usuario_nome])

            mensagem = f'<div class="alert alert-success">✅ Exame lançado por {usuario_nome}!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro no Caixa: {e}</div>'

    # ===============================
    # CADASTRO / EDIÇÃO EXAMES (COM AUDITORIA)
    # ===============================
    if request.method == "POST" and "salvar_exame" in request.POST:
        try:
            id_post = request.POST.get('id_exame')
            nome = request.POST.get('nome')
            grupo = request.POST.get('grupo')
            valor = request.POST.get('valor') or 0

            with connection.cursor() as cursor:
                if id_post:
                    # ✅ UPDATE NA TABELA EXAMES
                    cursor.execute("""
                        UPDATE exames SET nome=%s, grupo=%s, valor_particular=%s, usuario_lancamento=%s
                        WHERE id=%s
                    """, [nome, grupo, valor, usuario_nome, id_post])
                else:
                    # ✅ INSERT NA TABELA EXAMES (5 colunas)
                    cursor.execute("""
                        INSERT INTO exames (nome, grupo, valor_particular, usuario_lancamento)
                        VALUES (%s,%s,%s,%s)
                    """, [nome, grupo, valor, usuario_nome])

            return HttpResponseRedirect('/exames/')
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro no Cadastro: {e}</div>'

    # ===============================
    # BUSCAR DADOS (RESTANTE INALTERADO)
    # ===============================
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM exames ORDER BY nome")
        exames_data = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM prestadores ORDER BY nome")
        prestadores_data = cursor.fetchall()
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades_data = cursor.fetchall()
        cursor.execute("SELECT id, nome, grupo, valor_particular FROM exames ORDER BY nome")
        exames_lista = cursor.fetchall()

    opts_exames = "".join([f'<option value="{e[0]}">{e[1]}</option>' for e in exames_data])
    opts_prest = "".join([f'<option value="{p[1]}">{p[1]}</option>' for p in prestadores_data])
    opts_uni = "".join([f'<option value="{u[0]}">{u[1]}</option>' for u in unidades_data])

    linhas = "".join([f"<tr><td>{ex[1]}</td><td>{ex[2] or '-'}</td><td>R$ {float(ex[3] or 0):.2f}</td></tr>" for ex in exames_lista])

    conteudo = f"""
    <h4>🧪 Exames</h4>
    {mensagem}
    <div class="card p-3 mb-3 border-primary shadow-sm">
        <h6 class="fw-bold">Novo / Editar Exame</h6>
        <form method="POST" class="row g-2">
            <input type="hidden" name="id_exame" value="">
            <div class="col-md-4"><input type="text" name="nome" class="form-control" placeholder="Nome do exame" required></div>
            <div class="col-md-3"><input type="text" name="grupo" class="form-control" placeholder="Grupo"></div>
            <div class="col-md-2"><input type="number" step="0.01" name="valor" class="form-control" placeholder="Valor"></div>
            <div class="col-md-3"><button name="salvar_exame" class="btn btn-primary w-100">Salvar</button></div>
        </form>
    </div>

    <div class="card p-3 mb-3 border-success shadow-sm">
        <h5>💰 Caixa de Exames</h5>
        <form method="POST" class="row g-2">
            <div class="col-md-2"><select name="unidade_id" class="form-select" required><option value="">Unidade</option>{opts_uni}</select></div>
            <div class="col-md-2"><input type="text" name="paciente" class="form-control" placeholder="Paciente" required></div>
            <div class="col-md-2"><select name="exame_id" class="form-select" required><option value="">Exame</option>{opts_exames}</select></div>
            <div class="col-md-2"><select name="prestador" class="form-select"><option value="">Prestador</option>{opts_prest}</select></div>
            <div class="col-md-1"><input type="number" step="0.01" name="valor" class="form-control" placeholder="Valor"></div>
            <div class="col-md-2"><select name="forma" class="form-select"><option>Pix</option><option>Cartão</option><option>Dinheiro</option></select></div>
            <div class="col-md-1"><button name="lancar_exame" class="btn btn-success w-100">OK</button></div>
        </form>
    </div>

    <table class="table table-sm table-hover">
        <thead class="table-light"><tr><th>Exame</th><th>Grupo</th><th>Valor</th></tr></thead>
        <tbody>{linhas}</tbody>
    </table>
    """
    # ✅ CHAMADA CORRETA PARA O NOVO BASE_HTML
    return HttpResponse(base_html(request, "Exames", conteudo))












# --- 8. TELA 6: ODONTOLOGIA ---
# --- 8. TELA 6: ODONTOLOGIA + CAIXA ODONTO ---
@csrf_exempt
def odonto_geral(request):
    from django.db import connection
    from django.http import HttpResponse, HttpResponseRedirect
    import datetime

    mensagem = ""

    # ===============================
    # EXCLUIR PROCEDIMENTO
    # ===============================
    if request.GET.get('delete_odonto'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM odontologia WHERE id = %s", [request.GET.get('delete_odonto')])
        return HttpResponseRedirect('/odontologia/')

    # ===============================
    # CADASTRAR PRESTADOR
    # ===============================
    if request.method == "POST" and "novo_prestador" in request.POST:
        try:
            nome = request.POST.get('nome_prestador')

            if nome:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO prestadores (nome) VALUES (%s)", [nome])

                mensagem = '<div class="alert alert-success">✅ Prestador cadastrado!</div>'

        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ {e}</div>'

    # ===============================
    # LANÇAMENTO CAIXA ODONTO 🔥
    # ===============================
    if request.method == "POST" and "lancar_odonto" in request.POST:
        try:
            paciente = request.POST.get('paciente')
            odonto_id = request.POST.get('odonto_id')
            prestador = request.POST.get('prestador')
            valor = float(request.POST.get('valor') or 0)
            forma = request.POST.get('forma')
            unidade_id = request.POST.get('unidade_id')

            if not paciente or not odonto_id:
                raise Exception("Paciente e procedimento obrigatórios")

            if not unidade_id:
                raise Exception("Selecione a unidade")

            with connection.cursor() as cursor:

                cursor.execute("SELECT procedimento FROM odontologia WHERE id = %s", [odonto_id])
                od = cursor.fetchone()
                nome_proc = od[0] if od else "Procedimento"

                cursor.execute("""
                    INSERT INTO caixa
                    (paciente_nome, profissional_nome, valor, forma_pagamento, status, categoria, descricao, data_pagamento, unidade_id)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE,%s)
                """, [
                    paciente,
                    prestador,
                    valor,
                    forma,
                    'Pago',
                    'Odontologia',
                    nome_proc,
                    unidade_id
                ])

            mensagem = '<div class="alert alert-success">✅ Procedimento lançado no caixa!</div>'

        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ {e}</div>'

    # ===============================
    # CADASTRO / EDIÇÃO ODONTO
    # ===============================
    edit_id = request.GET.get('edit_odonto')
    o_dados = ["", "", 0.00, ""]

    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT procedimento, grupo, valor_particular, observacoes 
                FROM odontologia WHERE id = %s
            """, [edit_id])
            res = cursor.fetchone()
            if res:
                o_dados = res

    if request.method == "POST" and "salvar_odonto" in request.POST:
        try:
            id_post = request.POST.get('id_odonto')

            proc = request.POST.get('procedimento')
            grupo = request.POST.get('grupo')
            valor = request.POST.get('valor') or 0
            obs = request.POST.get('observacoes')

            with connection.cursor() as cursor:
                if id_post:
                    cursor.execute("""
                        UPDATE odontologia 
                        SET procedimento=%s, grupo=%s, valor_particular=%s, observacoes=%s
                        WHERE id=%s
                    """, [proc, grupo, valor, obs, id_post])
                else:
                    cursor.execute("""
                        INSERT INTO odontologia (procedimento, grupo, valor_particular, observacoes)
                        VALUES (%s,%s,%s,%s)
                    """, [proc, grupo, valor, obs])

            return HttpResponseRedirect('/odontologia/')

        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ {e}</div>'

    # ===============================
    # BUSCAR DADOS
    # ===============================
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, procedimento FROM odontologia ORDER BY procedimento")
        procedimentos = cursor.fetchall()

        cursor.execute("SELECT id, nome FROM prestadores ORDER BY nome")
        prestadores = cursor.fetchall()

        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()

        cursor.execute("""
            SELECT id, procedimento, grupo, valor_particular, observacoes 
            FROM odontologia ORDER BY procedimento
        """)
        lista_odonto = cursor.fetchall()

    # ===============================
    # SELECTS
    # ===============================
    opts_proc = "".join([f'<option value="{p[0]}">{p[1]}</option>' for p in procedimentos])
    opts_prest = "".join([f'<option value="{p[1]}">{p[1]}</option>' for p in prestadores])
    opts_uni = "".join([f'<option value="{u[0]}">{u[1]}</option>' for u in unidades])

    # ===============================
    # LISTA
    # ===============================
    linhas = ""
    for o in lista_odonto:
        linhas += f"""
        <tr>
            <td>{o[1]}</td>
            <td>{o[2] or '-'}</td>
            <td>R$ {float(o[3] or 0):.2f}</td>
            <td>{o[4] or '-'}</td>
        </tr>
        """

    # ===============================
    # HTML
    # ===============================
    conteudo = f"""
    <h4>🦷 Odontologia</h4>

    {mensagem}

    <!-- CADASTRO -->
    <div class="card p-3 mb-3">
        <form method="POST" class="row g-2">
            <input type="hidden" name="id_odonto" value="{edit_id or ''}">

            <div class="col-md-4">
                <input type="text" name="procedimento" class="form-control" placeholder="Procedimento" required>
            </div>

            <div class="col-md-3">
                <input type="text" name="grupo" class="form-control" placeholder="Grupo">
            </div>

            <div class="col-md-2">
                <input type="number" step="0.01" name="valor" class="form-control" placeholder="Valor">
            </div>

            <div class="col-md-3">
                <button name="salvar_odonto" class="btn btn-primary w-100">Salvar</button>
            </div>

            <div class="col-12">
                <textarea name="observacoes" class="form-control" placeholder="Observações"></textarea>
            </div>
        </form>
    </div>

    <!-- CAIXA ODONTO -->
    <div class="card p-3 mb-3 border-success">
        <h5>💰 Caixa Odontológico</h5>

        <form method="POST" class="row g-2">

            <div class="col-md-2">
                <select name="unidade_id" class="form-select" required>
                    <option value="">Unidade</option>
                    {opts_uni}
                </select>
            </div>

            <div class="col-md-2">
                <input type="text" name="paciente" class="form-control" placeholder="Paciente" required>
            </div>

            <div class="col-md-2">
                <select name="odonto_id" class="form-select" required>
                    <option value="">Procedimento</option>
                    {opts_proc}
                </select>
            </div>

            <div class="col-md-2">
                <select name="prestador" class="form-select">
                    <option value="">Prestador</option>
                    {opts_prest}
                </select>
            </div>

            <div class="col-md-1">
                <input type="number" step="0.01" name="valor" class="form-control" placeholder="Valor">
            </div>

            <div class="col-md-2">
                <select name="forma" class="form-select">
                    <option>Pix</option>
                    <option>Cartão</option>
                    <option>Dinheiro</option>
                </select>
            </div>

            <div class="col-md-1">
                <button name="lancar_odonto" class="btn btn-success w-100">OK</button>
            </div>

        </form>

        <!-- PRESTADOR -->
        <form method="POST" class="mt-2 d-flex gap-2">
            <input type="text" name="nome_prestador" class="form-control" placeholder="Novo prestador">
            <button name="novo_prestador" class="btn btn-secondary">Cadastrar</button>
        </form>
    </div>

    <!-- LISTA -->
    <table class="table table-sm">
        <tr><th>Procedimento</th><th>Grupo</th><th>Valor</th><th>Obs</th></tr>
        {linhas}
    </table>
    """

    return HttpResponse(base_html("Odontologia", conteudo))










# --- 9. TELA 7: PACIENTES ---
# --- 9. TELA 7: PACIENTES ---
@csrf_exempt
def pacientes_geral(request):
    from django.db import connection
    from django.http import HttpResponse, HttpResponseRedirect

    mensagem = ""
    
    # 1. BLOQUEAR
    if request.GET.get('block_pac'):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE pacientes SET status = 'Bloqueado' WHERE id = %s", [request.GET.get('block_pac')])
        return HttpResponseRedirect('/pacientes/')

    # 2. DESBLOQUEAR (NOVO)
    if request.GET.get('unblock_pac'):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE pacientes SET status = 'Ativo' WHERE id = %s", [request.GET.get('unblock_pac')])
        return HttpResponseRedirect('/pacientes/')

    # 3. EXCLUIR
    if request.GET.get('delete_pac'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM pacientes WHERE id = %s", [request.GET.get('delete_pac')])
        return HttpResponseRedirect('/pacientes/')

    # 4. EDITAR
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
                if p_dados[3]:
                    p_dados[3] = p_dados[3].strftime('%Y-%m-%d')

    # 5. SALVAR
    if request.method == "POST":
        id_post = request.POST.get('id_pac')

        cpf = request.POST.get('cpf')
        if not cpf or cpf.strip() == "":
            cpf = None

        campos = [
            request.POST.get('nome'),
            cpf,
            request.POST.get('sexo'),
            request.POST.get('data_nasc') or None,
            request.POST.get('telefone'),
            request.POST.get('convenio_id') or None,
            request.POST.get('cep'),
            request.POST.get('rua'),
            request.POST.get('numero'),
            request.POST.get('bairro'),
            request.POST.get('cidade'),
            request.POST.get('estado'),
            request.POST.get('observacoes')
        ]

        try:
            with connection.cursor() as cursor:
                if id_post:
                    cursor.execute("""
                        UPDATE pacientes SET 
                            nome=%s, cpf=%s, sexo=%s, data_nascimento=%s, telefone=%s, 
                            convenio_id=%s, cep=%s, rua=%s, numero=%s, bairro=%s, 
                            cidade=%s, estado=%s, observacoes=%s 
                        WHERE id=%s
                    """, campos + [id_post])
                else:
                    cursor.execute("""
                        INSERT INTO pacientes 
                        (nome, cpf, sexo, data_nascimento, telefone, convenio_id, cep, rua, numero, bairro, cidade, estado, observacoes) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, campos)

            return HttpResponse("""
                <html>
                    <head>
                        <script>
                            alert("Paciente Atualizado");
                            window.location.href = "/recepcao/";
                        </script>
                    </head>
                    <body></body>
                </html>
            """)

        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    # 6. BUSCA
    termo_busca = request.GET.get('busca', '')
    termo_sql = termo_busca

    if "/" in termo_busca:
        try:
            d, m, a = termo_busca.split('/')
            termo_sql = f"{a}-{m}-{d}"
        except:
            pass

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
            sql_busca += """
                WHERE p.cpf LIKE %s 
                OR CAST(p.data_nascimento AS TEXT) LIKE %s 
                OR p.nome ILIKE %s
                OR p.cidade ILIKE %s
            """
            params = [
                f'%{termo_sql}%',
                f'%{termo_sql}%',
                f'%{termo_busca}%',
                f'%{termo_busca}%'
            ]
        
        sql_busca += " ORDER BY p.id DESC"
        cursor.execute(sql_busca, params)
        lista_pacientes = cursor.fetchall()

    # 7. HTML
    opcoes_conv = "".join([
        f'<option value="{c[0]}" {"selected" if str(c[0])==str(p_dados[5]) else ""}>{c[1]}</option>'
        for c in convenios
    ])
    
    linhas = ""
    for p in lista_pacientes:
        cor_st = "success" if p[5] == "Ativo" else "danger"
        data_br = p[7].strftime('%d/%m/%Y') if p[7] else '--'
        
        linhas += f"""
        <tr>
            <td><b>{p[1]}</b><br><small class='text-muted'>CPF: {p[2]} | Nasc: {data_br}</small></td>
            <td>{p[3]}<br><span class="badge bg-{cor_st}">{p[5]}</span></td>
            <td>{p[4] if p[4] else 'Particular'}</td>
            <td>
                <div class="btn-group">
                    <a href="/pacientes/?edit_pac={p[0]}" class="btn btn-sm btn-info text-white" title="Editar Paciente">
                        <i class="bi bi-pencil"></i>
                    </a>
                    <a href="/pacientes/?block_pac={p[0]}" class="btn btn-sm btn-warning" title="Bloquear Paciente">
                        <i class="bi bi-slash-circle"></i>
                    </a>
                    <a href="/pacientes/?unblock_pac={p[0]}" class="btn btn-sm btn-success" title="Desbloquear Paciente">
                        <i class="bi bi-check-circle"></i>
                    </a>
                    <a href="/pacientes/?delete_pac={p[0]}" class="btn btn-sm btn-danger" onclick="return confirm('Excluir?')" title="Excluir Paciente">
                        <i class="bi bi-trash"></i>
                    </a>
                </div>
            </td>
        </tr>
        """

    conteudo = f"""
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4><i class="bi bi-people-fill"></i> Gestão de Pacientes</h4>
            <a href="/admin-painel/" class="btn btn-outline-secondary btn-sm">Painel</a>
        </div>
        
        {mensagem}

        <form method="POST" class="row g-2 mb-4 bg-light p-3 rounded border shadow-sm">
            <input type="hidden" name="id_pac" value="{edit_id or ''}">
            <div class="col-md-5"><label>Nome</label><input type="text" name="nome" class="form-control" value="{p_dados[0]}" required></div>
            <div class="col-md-3"><label>CPF</label><input type="text" name="cpf" class="form-control" value="{p_dados[1]}"></div>
            <div class="col-md-2"><label>Sexo</label>
                <select name="sexo" class="form-select">
                    <option value="Masculino" {"selected" if p_dados[2]=="Masculino" else ""}>M</option>
                    <option value="Feminino" {"selected" if p_dados[2]=="Feminino" else ""}>F</option>
                </select>
            </div>
            <div class="col-md-2"><label>Nascimento</label><input type="date" name="data_nasc" class="form-control" value="{p_dados[3]}" required></div>

            <div class="col-md-4"><label>Telefone</label><input type="text" name="telefone" class="form-control" value="{p_dados[4]}" required></div>
            <div class="col-md-4"><label>Convênio</label>
                <select name="convenio_id" class="form-select">
                    <option value="">Particular</option>
                    {opcoes_conv}
                </select>
            </div>
            <div class="col-md-4"><label>CEP</label><input type="text" name="cep" class="form-control" value="{p_dados[6]}"></div>

            <div class="col-md-5"><label>Rua</label><input type="text" name="rua" class="form-control" value="{p_dados[7]}"></div>
            <div class="col-md-2"><label>Nº</label><input type="text" name="numero" class="form-control" value="{p_dados[8]}"></div>
            <div class="col-md-5"><label>Bairro</label><input type="text" name="bairro" class="form-control" value="{p_dados[9]}"></div>

            <div class="col-md-4"><label>Cidade</label><input type="text" name="cidade" class="form-control" value="{p_dados[10]}"></div>
            <div class="col-md-2"><label>UF</label><input type="text" name="estado" class="form-control" value="{p_dados[11]}" maxlength="2"></div>
            <div class="col-md-6"><label>Observações</label><input type="text" name="observacoes" class="form-control" value="{p_dados[12]}"></div>

            <div class="col-12 mt-3">
                <button type="submit" class="btn btn-danger w-100">
                    {'ATUALIZAR DADOS' if edit_id else 'SALVAR NOVO PACIENTE'}
                </button>
            </div>
        </form>

        <form method="GET" class="mb-3">
            <input type="text" name="busca" class="form-control" value="{termo_busca}" placeholder="Buscar por Nome, CPF, Data ou Cidade">
        </form>

        <table class="table table-hover">
            <thead class="table-dark">
                <tr><th>Paciente</th><th>Contato</th><th>Convênio</th><th>Ações</th></tr>
            </thead>
            <tbody>{linhas}</tbody>
        </table>
    """

    return HttpResponse(base_html("Pacientes", conteudo))












# --- 10. TELA 8: ACESSOS ---
# --- 10. TELA 8: ACESSOS ---

from django.contrib.auth.decorators import login_required

@login_required
def acesso_geral(request):
    from django.db import connection
    from django.http import HttpResponse, HttpResponseRedirect
    from django.contrib.auth import get_user_model

    User = get_user_model()

    mensagem = ""
    
    # --- LISTAR UNIDADES ---
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()

    opcoes_unidades = "".join([
        f"<option value='{u[0]}'>{u[1]}</option>"
        for u in unidades
    ])

    if request.method == "POST":
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        cargo = request.POST.get('cargo')
        cpf = request.POST.get('cpf')
        unidade_id = request.POST.get('unidade_id')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'auth_user'
                    )
                """)
                tabela_existe = cursor.fetchone()[0]

            if not tabela_existe:
                mensagem = '<div class="alert alert-danger">❌ Execute migrate.</div>'
            else:
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username=username, password=senha)
                    
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """
                            INSERT INTO perfis_usuario 
                            (user_id, nome_completo, cargo, cpf, unidade_id) 
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            [user.id, nome, cargo, cpf, unidade_id]
                        )

                    mensagem = f'<div class="alert alert-success">✅ Usuário {username} criado!</div>'
                else:
                    mensagem = '<div class="alert alert-danger">❌ Login já existe</div>'

        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    # --- EXCLUIR (CORRIGIDO) ---
    if request.GET.get("delete"):
        user_id = request.GET.get("delete")
        try:
            with connection.cursor() as cursor:
                # remove perfil
                cursor.execute("DELETE FROM perfis_usuario WHERE user_id = %s", [user_id])
                # remove usuário direto (SEM ORM)
                cursor.execute("DELETE FROM auth_user WHERE id = %s", [user_id])

            return HttpResponseRedirect("/acessos/")

        except Exception as e:
            mensagem = f"<div class='alert alert-danger'>Erro ao excluir: {e}</div>"

    # --- LISTA FUNCIONÁRIOS ---
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.user_id, p.nome_completo, p.cargo, p.cpf, u.nome
            FROM perfis_usuario p
            LEFT JOIN unidades u ON p.unidade_id = u.id
            ORDER BY p.cargo, p.nome_completo
        """)
        funcionarios = cursor.fetchall()

    linhas = "".join([
        f"""
        <tr>
            <td>
                <b>{f[1]}</b><br>
                <a href="/acessos/?edit={f[0]}" class="btn btn-sm btn-info text-white mt-1">Editar</a>
                <a href="/acessos/?delete={f[0]}" class="btn btn-sm btn-danger mt-1"
                   onclick="return confirm('Excluir usuário?')">Excluir</a>
            </td>
            <td>{f[2]}</td>
            <td>{f[3]}</td>
            <td>{f[4] or '-'}</td>
        </tr>
        """
        for f in funcionarios
    ])

    conteudo = f"""
        <h4>Controle de Acesso</h4><hr>
        {mensagem}

        <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">

            <input name="nome" placeholder="Nome" class="form-control mb-2" required>
            <input name="username" placeholder="Usuário" class="form-control mb-2" required>
            <input name="senha" type="password" placeholder="Senha" class="form-control mb-2" required>

            <select name="cargo" class="form-control mb-2">
                <option>Recepção</option>
                <option>Médico</option>
                <option>Dentista</option>
                <option>Administrador</option>
            </select>

            <select name="unidade_id" class="form-control mb-2">
                <option value="">Selecione a Unidade</option>
                {opcoes_unidades}
            </select>

            <input name="cpf" placeholder="CPF" class="form-control mb-2">

            <button class="btn btn-dark w-100">Criar</button>
        </form>

        <hr>

        <table class="table">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Cargo</th>
                    <th>CPF</th>
                    <th>Unidade</th>
                </tr>
            </thead>
            {linhas}
        </table>
    """

    return HttpResponse(base_html("Acessos", conteudo))













# --- 11. TELA 9: TABELA DE PREÇOS DE CONSTULTAS ---
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






# --- 12. TELA 10: PREÇOS DE EXAMES ---
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







# --- 13. TELA 11: CONFIGURAÇÃO DE AGENDAS (ABRIR GRADES) ---
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


# --- 14. TELA 12: AGENDA GERAL CONSULTAS ---
# --- 14. TELA 12: AGENDA GERAL (COM COLUNA QUEM AGENDOU) ---
@csrf_exempt
def agenda_diaria(request):
    import datetime, urllib.parse
    hoje_str = datetime.date.today().strftime('%Y-%m-%d')
    data_sel = request.GET.get('data') or hoje_str
    unidade_id = request.GET.get('unidade')
    
    try:
        with connection.cursor() as cursor:
            # 1. BUSCAR UNIDADES
            cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
            unidades = cursor.fetchall()

            # 2. BUSCAR AGENDAMENTOS EXISTENTES
            sql_ocupados = """
                SELECT 
                    ag.horario_selecionado, 
                    pac.nome, 
                    prof.nome, 
                    conv.nome, 
                    pac.telefone, 
                    u.nome, 
                    u.endereco,
                    esp.nome,
                    ag.id
                FROM agendamentos ag
                JOIN pacientes pac ON ag.paciente_id = pac.id
                JOIN agendas_config ac ON ag.agenda_config_id = ac.id
                JOIN profissionais prof ON ac.profissional_id = prof.id
                JOIN unidades u ON ac.unidade_id = u.id
                LEFT JOIN especialidades esp ON prof.especialidade_id = esp.id
                LEFT JOIN convenios conv ON pac.convenio_id = conv.id
                WHERE ag.data_agendamento = %s
            """
            params_oc = [data_sel]
            if unidade_id:
                sql_ocupados += " AND u.id = %s"
                params_oc.append(unidade_id)
            
            cursor.execute(sql_ocupados, params_oc)
            agendados = cursor.fetchall()

            dict_ocupados = {}
            for a in agendados:
                hora_key = a[0].strftime('%H:%M') if not isinstance(a[0], str) else a[0][:5]
                dict_ocupados[hora_key] = {
                    "paciente": a[1], "medico": a[2], "convenio": a[3] or "Particular",
                    "tel": a[4], "unidade": a[5], "endereco": a[6], "especialidade": a[7], "id": a[8]
                }

            # 3. BUSCAR GRADES
            sql_grades = """
                SELECT ac.id, prof.nome, ac.horario_inicio, ac.horario_fim, ac.intervalo_minutos, u.nome
                FROM agendas_config ac
                JOIN profissionais prof ON ac.profissional_id = prof.id
                JOIN unidades u ON ac.unidade_id = u.id
                WHERE ac.data_especifica = %s
            """
            params_gr = [data_sel]
            if unidade_id:
                sql_grades += " AND u.id = %s"
                params_gr.append(unidade_id)
            
            cursor.execute(sql_grades, params_gr)
            grades = cursor.fetchall()

        # 4. GERAR LISTA DE HORÁRIOS
        lista_final = []
        for g in grades:
            id_conf, nome_p, h_ini, h_fim, inter, u_nome = g
            inter = inter or 20
            
            atual = datetime.datetime.combine(datetime.date.today(), h_ini)
            fim = datetime.datetime.combine(datetime.date.today(), h_fim)
            
            while atual.time() < fim.time():
                h_str = atual.strftime('%H:%M')
                
                if h_str in dict_ocupados:
                    dados = dict_ocupados[h_str]
                    
                    # --- LÓGICA DE SEPARAÇÃO DE NOMES ---
                    nome_completo = dados['paciente'] or "---"
                    nome_paciente = nome_completo
                    quem_agendou = "Próprio"

                    if "(Ag: " in nome_completo:
                        partes = nome_completo.split("(Ag: ")
                        nome_paciente = partes[0].strip()
                        quem_agendou = partes[1].replace(")", "").strip()

                    tel_limpo = "".join(filter(str.isdigit, str(dados['tel'] or "")))
                    # Mensagem Zap sempre com o nome limpo
                    msg = f"Olá, {nome_paciente}. Gentileza confirmar consulta com {dados['medico']} ({dados['especialidade']}) hoje às {h_str} na unidade {dados['unidade']} - {dados['endereco']}"
                    link_zap = f"https://wa.me/55{tel_limpo}?text={urllib.parse.quote(msg)}"
                    
                    lista_final.append({
                        "hora": h_str, "medico": dados['medico'], "paciente": nome_paciente,
                        "quem_agendou": quem_agendou, "convenio": dados['convenio'], 
                        "tel": dados['tel'], "status": "Ocupado", "zap": link_zap
                    })
                else:
                    lista_final.append({
                        "hora": h_str, "medico": nome_p, "paciente": "---",
                        "quem_agendou": "---", "convenio": "---", "tel": "---", "status": "Livre", "zap": None
                    })
                atual += datetime.timedelta(minutes=inter)

        # 5. MONTAR TABELA
        linhas = ""
        for item in sorted(lista_final, key=lambda x: x['hora']):
            col_acoes = ""
            if item['status'] == "Ocupado":
                col_acoes = f"""
                    <div class="d-flex align-items-center gap-2">
                        <input type="checkbox" class="form-check-input border-primary" title="Confirmado?">
                        <a href="{item['zap']}" target="_blank" class="btn btn-sm btn-success py-0 shadow-sm">
                            <i class="bi bi-whatsapp"></i> Zap
                        </a>
                    </div>
                """
            else:
                col_acoes = f'<a href="/agendar/?hora={item["hora"]}&prof={item["medico"]}&data={data_sel}" class="btn btn-sm btn-outline-primary py-0">Agendar</a>'

            linhas += f"""
                <tr>
                    <td><b class="text-primary">{item['hora']}</b></td>
                    <td>{item['medico']}</td>
                    <td>{item['paciente']}</td>
                    <td class="text-muted small">{item['quem_agendou']}</td>
                    <td><small>{item['convenio']}</small></td>
                    <td><small>{item['tel']}</small></td>
                    <td>{col_acoes}</td>
                </tr>"""

        opts_unidades = "".join([f'<option value="{u[0]}" {"selected" if str(unidade_id)==str(u[0]) else ""}>{u[1]}</option>' for u in unidades])

        conteudo = f"""
            <div class="container-fluid py-3">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h4 class="fw-bold"><i class="bi bi-calendar3 text-primary"></i> Agenda Geral</h4>
                    <span class="badge bg-dark">Horários: {len(lista_final)}</span>
                </div>

                <form method="GET" class="row g-2 mb-4 bg-light p-3 rounded border shadow-sm">
                    <div class="col-md-3">
                        <label class="small fw-bold">Unidade</label>
                        <select name="unidade" class="form-select border-primary shadow-sm">
                            <option value="">Todas as Unidades</option>{opts_unidades}
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label class="small fw-bold">Data</label>
                        <input type="date" name="data" value="{data_sel}" class="form-control border-primary shadow-sm">
                    </div>
                    <div class="col-md-2 d-flex align-items-end">
                        <button class="btn btn-primary w-100 fw-bold shadow-sm">BUSCAR</button>
                    </div>
                </form>

                <div class="table-responsive card shadow border-0 overflow-hidden">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-dark">
                            <tr>
                                <th>Hora</th>
                                <th>Profissional</th>
                                <th>Paciente</th>
                                <th>Quem Agendou</th>
                                <th>Convênio</th>
                                <th>Telefone</th>
                                <th>Ações / Confirmação</th>
                            </tr>
                        </thead>
                        <tbody style="font-size: 0.9rem;">
                            {linhas if linhas else '<tr><td colspan="7" class="text-center py-5">Nenhuma grade aberta.</td></tr>'}
                        </tbody>
                    </table>
                </div>
            </div>
        """
        return HttpResponse(base_html("Agenda Geral", conteudo))

    except Exception as e:
        return HttpResponse(base_html("Erro", f"<h4>Erro:</h4><pre>{e}</pre>"))







# --- 15. TELA 13: NOVO AGENDAMENTO ---
# --- TELA 13: NOVO AGENDAMENTO (COM TRAVA DE CLIQUE DUPLO) ---
@csrf_exempt
def agendar_consulta(request):
    mensagem = ""
    hoje = datetime.date.today()

    if request.GET.get('sucesso'):
        conteudo_sucesso = f"""
            <div class="container py-5 text-center">
                <div class="card shadow-lg p-4 border-0">
                    <div class="display-1 text-success mb-3"><i class="bi bi-check-circle-fill"></i></div>
                    <h2 class="fw-bold">Agendamento Realizado!</h2>
                    <hr>
                    <a href="{request.path}" class="btn btn-primary btn-lg fw-bold shadow">NOVO AGENDAMENTO</a>
                    <br><br>
                    <a href="/admin-painel/" class="text-secondary small">Voltar ao Painel</a>
                </div>
            </div>
        """
        return HttpResponse(base_html("Sucesso", conteudo_sucesso))

    unid_id = request.GET.get('unidade_id')
    esp_id = request.GET.get('especialidade_id')
    prof_id = request.GET.get('profissional_id')
    data_sel = request.GET.get('data_sel') 
    hora_sel = request.GET.get('hora_sel')

    with connection.cursor() as cursor:
        # 🔹 1. UNIDADES
        cursor.execute("""
            SELECT DISTINCT u.id, u.nome FROM unidades u 
            JOIN agendas_config ac ON u.id = ac.unidade_id 
            WHERE ac.data_especifica >= %s ORDER BY u.nome
        """, [hoje])
        unidades = cursor.fetchall()

        # 🔹 2. ESPECIALIDADES
        especialidades = []
        if unid_id:
            cursor.execute("""
                SELECT DISTINCT e.id, e.nome FROM especialidades e 
                JOIN profissionais p ON e.id = p.especialidade_id 
                JOIN agendas_config ac ON p.id = ac.profissional_id 
                WHERE ac.unidade_id = %s AND ac.data_especifica >= %s ORDER BY e.nome
            """, [unid_id, hoje])
            especialidades = cursor.fetchall()

        # 🔹 3. PROFISSIONAIS
        profs_filtrados = []
        if unid_id and esp_id:
            cursor.execute("""
                SELECT DISTINCT p.id, p.nome FROM profissionais p 
                JOIN agendas_config ac ON p.id = ac.profissional_id 
                WHERE ac.unidade_id = %s AND p.especialidade_id = %s AND ac.data_especifica >= %s ORDER BY p.nome
            """, [unid_id, esp_id, hoje])
            profs_filtrados = cursor.fetchall()

        # 🔹 4. DATAS
        datas_disponiveis = []
        agenda_existe = True
        
        if prof_id and unid_id:
            cursor.execute("""
                SELECT data_especifica, horario_inicio, horario_fim, intervalo_minutos, id 
                FROM agendas_config 
                WHERE profissional_id = %s AND unidade_id = %s AND data_especifica >= %s 
                ORDER BY data_especifica
            """, [prof_id, unid_id, hoje])
            grades_candidatas = cursor.fetchall()
            
            if not grades_candidatas:
                agenda_existe = False
            
            for gf in grades_candidatas:
                d_grade, h_ini, h_fim, inter, g_id = gf
                total_minutos = (datetime.datetime.combine(hoje, h_fim) - datetime.datetime.combine(hoje, h_ini)).seconds / 60
                slots_possiveis = total_minutos / (inter or 20)
                
                cursor.execute("SELECT count(*) FROM agendamentos WHERE agenda_config_id = %s AND data_agendamento = %s AND status != 'Cancelado'", [g_id, d_grade])
                total_ocupados = cursor.fetchone()[0]
                
                if total_ocupados < slots_possiveis:
                    datas_disponiveis.append(d_grade)
            
            if grades_candidatas and not datas_disponiveis:
                agenda_existe = False

        # 🔹 5. HORÁRIOS
        horarios_list = []
        if prof_id and data_sel and unid_id:
            cursor.execute("""
                SELECT horario_inicio, horario_fim, intervalo_minutos, id 
                FROM agendas_config 
                WHERE profissional_id = %s AND data_especifica = %s AND unidade_id = %s
            """, [prof_id, data_sel, unid_id])
            grade = cursor.fetchone()
            
            if grade:
                d_obj = datetime.datetime.strptime(data_sel, '%Y-%m-%d').date()
                inicio = datetime.datetime.combine(d_obj, grade[0])
                fim = datetime.datetime.combine(d_obj, grade[1])
                intervalo = datetime.timedelta(minutes=grade[2] or 20)
                
                cursor.execute("SELECT horario_selecionado FROM agendamentos WHERE agenda_config_id = %s AND data_agendamento = %s AND status != 'Cancelado'", [grade[3], data_sel])
                ocupados = [r[0].strftime('%H:%M') if not isinstance(r[0], str) else r[0][:5] for r in cursor.fetchall()]
                
                atual = inicio
                while atual < fim:
                    h_str = atual.strftime('%H:%M')
                    if h_str not in ocupados: horarios_list.append(h_str)
                    atual += intervalo

        cursor.execute("SELECT id, nome FROM convenios ORDER BY nome")
        lista_convenios = cursor.fetchall()

    # --- POST / SALVAMENTO ---
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM agendas_config WHERE profissional_id = %s AND data_especifica = %s AND unidade_id = %s", [prof_id, data_sel, unid_id])
                id_conf_save = cursor.fetchone()[0]
                nome_pac = request.POST.get('nome')
                quem_agenda = request.POST.get('quem_agenda')
                whatsapp = request.POST.get('whatsapp')
                conv_id = request.POST.get('convenio_id') or None
                nome_completo = f"{nome_pac} (Ag: {quem_agenda})" if quem_agenda else nome_pac
                cursor.execute("INSERT INTO pacientes (nome, telefone, convenio_id) VALUES (%s, %s, %s) RETURNING id", [nome_completo, whatsapp, conv_id])
                paciente_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO agendamentos (paciente_id, agenda_config_id, data_agendamento, horario_selecionado, status) VALUES (%s, %s, %s, %s, 'Agendado')", [paciente_id, id_conf_save, data_sel, hora_sel])
            return HttpResponseRedirect(f"{request.path}?sucesso=1")
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    # --- HTML DINÂMICO ---
    opts_unid = "".join([f'<option value="{u[0]}" {"selected" if str(u[0])==unid_id else ""}>{u[1]}</option>' for u in unidades])
    opts_esp = "".join([f'<option value="{e[0]}" {"selected" if str(e[0])==esp_id else ""}>{e[1]}</option>' for e in especialidades])
    opts_prof = "".join([f'<option value="{p[0]}" {"selected" if str(p[0])==prof_id else ""}>{p[1]}</option>' for p in profs_filtrados])
    opts_datas = "".join([f'<option value="{d}" {"selected" if str(d)==data_sel else ""}>{d.strftime("%d/%m/%Y")}</option>' for d in datas_disponiveis])
    
    label_data = "4. Data Disponível"
    placeholder_data = "Selecione..."
    estilo_data = "border-danger"
    if prof_id and not agenda_existe:
        placeholder_data = "⚠️ Agenda não aberta"
        estilo_data = "border-warning bg-warning-subtle"

    btns_horas = "".join([f'<a href="?unidade_id={unid_id}&especialidade_id={esp_id}&profissional_id={prof_id}&data_sel={data_sel}&hora_sel={h}" class="btn btn-sm m-1 {"btn-primary shadow" if h==hora_sel else "btn-outline-primary"}">{h}</a>' for h in horarios_list])

    # Script para bloquear múltiplos envios
    script_bloqueio = """
        <script>
        function bloquearBotao(form) {
            const btn = form.querySelector('button[type="submit"]');
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Processando...';
            return true;
        }
        </script>
    """

    conteudo = f"""
        {script_bloqueio}
        <div class="container py-3">
            <h4 class="text-center mb-4 fw-bold"><i class="bi bi-calendar-check text-primary"></i> Novo Agendamento</h4>
            {mensagem}
            <div class="card p-3 shadow-sm border-0 bg-light mb-4">
                <form method="GET" class="row g-2">
                    <div class="col-md-3"><label class="small fw-bold">1. Unidade</label><select name="unidade_id" class="form-select border-primary" onchange="this.form.submit()"><option value="">Selecione...</option>{opts_unid}</select></div>
                    <div class="col-md-3"><label class="small fw-bold">2. Especialidade</label><select name="especialidade_id" class="form-select border-primary" onchange="this.form.submit()" {"disabled" if not unid_id else ""}><option value="">Selecione...</option>{opts_esp}</select></div>
                    <div class="col-md-3"><label class="small fw-bold">3. Profissional</label><select name="profissional_id" class="form-select border-primary" onchange="this.form.submit()" {"disabled" if not esp_id else ""}><option value="">Selecione...</option>{opts_prof}</select></div>
                    <div class="col-md-3"><label class="small fw-bold text-danger">{label_data}</label><select name="data_sel" class="form-select {estilo_data}" onchange="this.form.submit()" {"disabled" if not datas_disponiveis else ""}><option value="">{placeholder_data}</option>{opts_datas}</select></div>
                </form>
            </div>
            {f'<div class="card p-3 shadow-sm mb-4 text-center border-0"><h6>Horários em {datetime.datetime.strptime(data_sel, "%Y-%m-%d").strftime("%d/%m/%Y") if data_sel else ""}</h6><div class="d-flex flex-wrap justify-content-center">{btns_horas if horarios_list else "Sem horários livres."}</div></div>' if data_sel else ""}
            {f'''<div class="card p-4 shadow border-success">
                <form method="POST" class="row g-3" onsubmit="return bloquearBotao(this)">
                    <div class="col-md-6"><label class="small fw-bold">Paciente</label><input type="text" name="nome" class="form-control" required></div>
                    <div class="col-md-6"><label class="small fw-bold">Quem Agendando?</label><input type="text" name="quem_agenda" class="form-control" required></div>
                    <div class="col-md-6"><label class="small fw-bold">WhatsApp</label><input type="text" name="whatsapp" class="form-control" required></div>
                    <div class="col-md-6"><label class="small fw-bold">Convênio</label><select name="convenio_id" class="form-select">{"".join([f"<option value='{c[0]}'>{c[1]}</option>" for c in lista_convenios])}</select></div>
                    <div class="col-12 mt-3"><button type="submit" class="btn btn-success w-100 fw-bold shadow">CONFIRMAR PARA {hora_sel}</button></div>
                </form>
            </div>''' if hora_sel else ""}
        </div>
    """
    return HttpResponse(base_html("Agendar", conteudo))








# --- 16. TELA 14: RECEPÇÃO CHECK-IN INTEGRADA COM PRONTUARIO ---
# --- 16. TELA 14: RECEPÇÃO CHECK-IN INTEGRADA COM PRONTUÁRIO ---
@csrf_exempt
def recepcao_geral(request):
    from django.db import connection
    from django.http import HttpResponse
    from django.shortcuts import redirect
    import datetime

    data_hoje = datetime.date.today()

    unidade_filtro = request.POST.get('unidade_id_hidden') or request.GET.get('unidade') or ""
    agendamento_id = request.GET.get('fluxo_id')
    etapa = request.GET.get('etapa', '1')

    mensagem = ""

    # ===============================
    # FINALIZAR CHECK-IN
    # ===============================
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

                descricao = "Retorno" if retorno else None

                if tipo == "avista":
                    valor = float(request.POST.get('valor') or 0)
                    if valor <= 0:
                        raise Exception("Informe o valor")

                    forma = request.POST.get('forma_pagamento') or "Pix"

                    cursor.execute("""
                        INSERT INTO caixa
                        (paciente_nome, profissional_nome, valor, forma_pagamento, status, categoria, descricao, data_pagamento, unidade_id)
                        VALUES (%s,%s,%s,%s,'Pago','Consulta',%s,CURRENT_DATE,%s)
                    """, [paciente_nome, profissional_nome, valor, forma, "Particular", unidade_id])

                elif tipo == "convenio":
                    convenio_nome = ""
                    if convenio_id:
                        cursor.execute("SELECT nome FROM convenios WHERE id = %s", [convenio_id])
                        c = cursor.fetchone()
                        if c:
                            convenio_nome = c[0]

                    cursor.execute("""
                        INSERT INTO caixa
                        (paciente_nome, profissional_nome, valor, forma_pagamento, status, categoria, descricao, data_pagamento, unidade_id)
                        VALUES (%s,%s,0,'Faturado','A Faturar','Consulta',%s,CURRENT_DATE,%s)
                    """, [paciente_nome, profissional_nome, descricao or convenio_nome or "Convênio", unidade_id])

                elif tipo == "cartao":
                    valor = float(request.POST.get('valor') or 0)
                    if valor <= 0:
                        raise Exception("Informe o valor")

                    forma = request.POST.get('forma_pagamento') or "Pix"

                    convenio_nome = ""
                    if convenio_id:
                        cursor.execute("SELECT nome FROM convenios WHERE id = %s", [convenio_id])
                        c = cursor.fetchone()
                        if c:
                            convenio_nome = c[0]

                    cursor.execute("""
                        INSERT INTO caixa
                        (paciente_nome, profissional_nome, valor, forma_pagamento, status, categoria, descricao, data_pagamento, unidade_id)
                        VALUES (%s,%s,%s,%s,'Pago','Consulta',%s,CURRENT_DATE,%s)
                    """, [
                        paciente_nome,
                        profissional_nome,
                        valor,
                        forma,
                        f"Cartão: {convenio_nome}" if convenio_nome else "Cartão Desconto",
                        unidade_id
                    ])

                cursor.execute("""
                    UPDATE agendamentos
                    SET status = 'Chegada'
                    WHERE id = %s
                """, [ag_id])

            return redirect(f"/recepcao/?unidade={unidade_filtro}")

        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ {e}</div>'

    # ===============================
    # BUSCAS (CORRIGIDO FILTRO)
    # ===============================
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()

        cursor.execute("SELECT id, nome FROM convenios ORDER BY nome")
        convenios = cursor.fetchall()

        # 🔴 CORREÇÃO AQUI
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
            sql += " AND u.id = %s"
            params.append(unidade_filtro)

        sql += " ORDER BY ag.horario_selecionado"

        cursor.execute(sql, params)
        agenda = cursor.fetchall()

    opts_unidades = "".join([
        f'<option value="{u[0]}" {"selected" if str(unidade_filtro)==str(u[0]) else ""}>{u[1]}</option>'
        for u in unidades
    ])

    opts_conv = "".join([f'<option value="{c[0]}">{c[1]}</option>' for c in convenios])

    linhas = ""
    for a in agenda:
        status = a[4] or "Agendado"

        if status == "Agendado":
            btn_acao = f'<a href="?fluxo_id={a[0]}&etapa=2&unidade={unidade_filtro}" class="btn btn-warning btn-sm">Check-in</a>'
        elif status == "Chegada":
            btn_acao = f'<a href="/prontuario/?id={a[0]}" class="btn btn-success btn-sm">Prontuário</a>'
        else:
            btn_acao = f'<span class="badge bg-secondary">{status}</span>'

        linhas += f"""
        <tr>
            <td>{str(a[3])[:5]}</td>
            <td>{a[1]}</td>
            <td>{a[2]}</td>
            <td>{btn_acao}</td>
        </tr>
        """

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
                                <option>Pix</option>
                                <option>Cartão</option>
                                <option>Dinheiro</option>
                            </select>
                        </div>

                        <button name="finalizar_fluxo" class="btn btn-success w-100">FINALIZAR</button>
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

            if (tipo === "convenio") {{
                pag.style.display = "none";
                conv.style.display = "block";
                ret.style.display = "block";
            }} else if (tipo === "cartao") {{
                pag.style.display = "block";
                conv.style.display = "block";
                ret.style.display = "none";
            }} else {{
                pag.style.display = "block";
                conv.style.display = "none";
                ret.style.display = "none";
            }}
        }}
        toggle();
        </script>
        """

    conteudo = f"""
    <h4>Recepção</h4>

    <form method="GET">
        <select name="unidade" class="form-select mb-2" onchange="this.form.submit()">
            <option value="">Todas</option>
            {opts_unidades}
        </select>
    </form>

    {mensagem}

    <table class="table">
        <tr><th>Hora</th><th>Paciente</th><th>Médico</th><th>Ação</th></tr>
        {linhas}
    </table>

    {modal_html}
    """

    return HttpResponse(base_html("Recepção", conteudo))











# --- 17. TELA 15: PRONTUÁRIO ---
# --- 17. TELA 15: PRONTUÁRIO (COM CONSULTA + VISUAL COMPLETO) ---
@csrf_exempt
def prontuario_geral(request):
    from django.db import connection
    from django.http import HttpResponse, HttpResponseRedirect

    agendamento_id = request.GET.get('id')
    consultar = request.GET.get('consultar')
    busca = request.GET.get('busca') or ""
    ver = request.GET.get('ver')  # 👈 NOVO (abrir completo)
    mensagem = ""

    # ===============================
    # 👁️ VISUALIZAÇÃO COMPLETA
    # ===============================
    if ver:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    p.nome,
                    pr.data_atendimento,
                    prof.nome,
                    pr.queixa,
                    pr.diagnostico,
                    pr.procedimentos
                FROM prontuarios pr
                JOIN pacientes p ON pr.paciente_id = p.id
                JOIN profissionais prof ON pr.profissional_id = prof.id
                WHERE pr.id = %s
            """, [ver])

            d = cursor.fetchone()

        if not d:
            return HttpResponse(base_html("Erro", "Prontuário não encontrado."))

        data = d[1].strftime('%d/%m/%Y') if d[1] else ""

        conteudo = f"""
        <div class="container py-4">
            <h4>📄 Prontuário Completo</h4>

            <a href="?consultar=1" class="btn btn-secondary mb-3">⬅ Voltar</a>

            <div class="card p-4 shadow-sm">
                <p><b>Paciente:</b> {d[0]}</p>
                <p><b>Data:</b> {data}</p>
                <p><b>Médico:</b> {d[2]}</p>

                <hr>

                <p><b>Histórico:</b><br>
                <div style="white-space:pre-wrap;">{d[3]}</div></p>

                <p><b>Diagnóstico:</b><br>
                <div style="white-space:pre-wrap;">{d[4]}</div></p>

                <p><b>Tratamento:</b><br>
                <div style="white-space:pre-wrap;">{d[5]}</div></p>
            </div>
        </div>
        """

        return HttpResponse(base_html("Prontuário Completo", conteudo))

    # ===============================
    # 🔎 CONSULTA DE PRONTUÁRIOS
    # ===============================
    if consultar:
        with connection.cursor() as cursor:

            sql = """
                SELECT 
                    pr.id,
                    p.nome,
                    pr.data_atendimento,
                    prof.nome,
                    pr.queixa,
                    pr.diagnostico,
                    pr.procedimentos
                FROM prontuarios pr
                JOIN pacientes p ON pr.paciente_id = p.id
                JOIN profissionais prof ON pr.profissional_id = prof.id
                WHERE 1=1
            """

            params = []

            if busca:
                sql += " AND p.nome ILIKE %s"
                params.append(f"%{busca}%")

            sql += " ORDER BY p.nome ASC"

            cursor.execute(sql, params)
            dados = cursor.fetchall()

        linhas = ""
        for d in dados:
            data = d[2].strftime('%d/%m/%Y') if d[2] else ""

            linhas += f"""
            <tr>
                <td><b>{d[1]}</b></td>
                <td>{data}</td>
                <td>{d[3]}</td>

                <td><div style="max-height:100px; overflow:auto;">{d[4]}</div></td>
                <td><div style="max-height:100px; overflow:auto;">{d[5]}</div></td>
                <td><div style="max-height:100px; overflow:auto;">{d[6]}</div></td>

                <td>
                    <a href="?consultar=1&ver={d[0]}" 
                       class="btn btn-sm btn-primary">
                       Abrir Completo
                    </a>
                </td>
            </tr>
            """

        conteudo = f"""
        <div class="container py-3">
            <h4>📋 Prontuários</h4>

            <form method="GET" class="row mb-3">
                <input type="hidden" name="consultar" value="1">

                <div class="col-md-10">
                    <input type="text" name="busca" value="{busca}" 
                        class="form-control" placeholder="Buscar por paciente...">
                </div>

                <div class="col-md-2">
                    <button class="btn btn-primary w-100">Buscar</button>
                </div>
            </form>

            <a href="/recepcao/" class="btn btn-secondary mb-3">Voltar</a>

            <div style="overflow-x:auto;">
                <table class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Paciente</th>
                            <th>Data</th>
                            <th>Médico</th>
                            <th>Histórico</th>
                            <th>Diagnóstico</th>
                            <th>Tratamento</th>
                            <th>Ação</th>
                        </tr>
                    </thead>

                    <tbody>
                        {linhas or '<tr><td colspan="7" class="text-center">Sem registros</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>
        """

        return HttpResponse(base_html("Consulta Prontuários", conteudo))

    # ===============================
    # 🔒 VALIDAÇÃO
    # ===============================
    if not agendamento_id:
        return HttpResponse(base_html("Erro", "ID do agendamento não informado."))

    # ===============================
    # DADOS DO ATENDIMENTO
    # ===============================
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id, p.nome, p.telefone, c.nome, pr.id, pr.nome, ag.data_agendamento, ag.horario_selecionado
            FROM agendamentos ag
            JOIN pacientes p ON ag.paciente_id = p.id
            LEFT JOIN convenios c ON p.convenio_id = c.id
            JOIN agendas_config ac ON ag.agenda_config_id = ac.id
            JOIN profissionais pr ON ac.profissional_id = pr.id
            WHERE ag.id = %s
        """, [agendamento_id])

        dados = cursor.fetchone()

        if not dados:
            return HttpResponse(base_html("Erro", "Agendamento não encontrado."))

        pac_id, pac_nome_bruto, pac_tel, conv_nome, prof_id, prof_nome, data, hora = dados
        pac_nome = pac_nome_bruto.split("(Ag:")[0].strip() if "(Ag:" in pac_nome_bruto else pac_nome_bruto

    # ===============================
    # 💾 SALVAR
    # ===============================
    if request.method == "POST":
        historico = request.POST.get('historico')
        diagnostico = request.POST.get('diagnostico')
        tratamento = request.POST.get('tratamento')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO prontuarios 
                    (paciente_id, profissional_id, data_atendimento, hora, queixa, anamnese, diagnostico, procedimentos, observacoes)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, [
                    pac_id,
                    prof_id,
                    data,
                    hora,
                    historico,
                    historico,
                    diagnostico,
                    tratamento,
                    ""
                ])

                cursor.execute("UPDATE agendamentos SET status = 'Finalizado' WHERE id = %s", [agendamento_id])

            return HttpResponseRedirect('/recepcao/')

        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro ao salvar: {e}</div>'

    # ===============================
    # HISTÓRICO LATERAL
    # ===============================
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT data_atendimento, diagnostico, procedimentos, queixa 
            FROM prontuarios 
            WHERE paciente_id = %s 
            ORDER BY data_atendimento DESC
        """, [pac_id])

        historico_lista = cursor.fetchall()

    lista_hist = ""
    for h in historico_lista:
        lista_hist += f"""
        <div class="card mb-2 border-start border-primary border-4 shadow-sm">
            <div class="card-body py-2">
                <small class="fw-bold text-primary">{h[0].strftime('%d/%m/%Y')}</small><br>
                <b>Histórico:</b> {h[3]}<br>
                <b>Diagnóstico:</b> {h[1]}
            </div>
        </div>
        """

    # ===============================
    # HTML PRINCIPAL
    # ===============================
    conteudo = f"""
    <div class="container py-3">

        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4>Atendimento Profissional</h4>

            <div>
                <a href="?consultar=1" class="btn btn-info btn-sm me-2">
                    📋 Consultar Prontuários
                </a>

                <a href="/recepcao/" class="btn btn-outline-secondary btn-sm">
                    Sair sem salvar
                </a>
            </div>
        </div>

        {mensagem}

        <div class="row">
            <div class="col-md-8">
                <div class="card p-3 mb-3">
                    <b>Paciente:</b> {pac_nome}<br>
                    <b>Convênio:</b> {conv_nome or 'Particular'}
                </div>

                <form method="POST">
                    <label>Histórico</label>
                    <textarea name="historico" class="form-control mb-2" required></textarea>

                    <label>Diagnóstico</label>
                    <textarea name="diagnostico" class="form-control mb-2"></textarea>

                    <label>Tratamento</label>
                    <textarea name="tratamento" class="form-control mb-3"></textarea>

                    <button class="btn btn-primary w-100">Salvar</button>
                </form>
            </div>

            <div class="col-md-4">
                <h6>Histórico do Paciente</h6>
                {lista_hist or 'Sem histórico'}
            </div>
        </div>
    </div>
    """

    return HttpResponse(base_html("Prontuário", conteudo))











# --- 18. TELA 16: CAIXA ---
# --- 18. TELA 16: CAIXA ---
# --- 18. TELA 16: CAIXA ---

@login_required
@csrf_exempt
def caixa_geral(request):
    from django.db import connection
    from django.http import HttpResponse
    import datetime
    import re
    import urllib.parse

    hoje = datetime.date.today()
    unidade_id = request.GET.get('unidade') or ""
    data_ini = request.GET.get('data_ini') or ""
    data_fim = request.GET.get('data_fim') or ""
    busca = request.GET.get('busca') or ""
    mensagem = ""

    # ===============================
    # FUNÇÕES AUXILIARES
    # ===============================
    def limpar_nome(nome):
        if not nome:
            return ""
        return re.sub(r"\(.*?\)", "", nome).strip()

    def br_to_sql(data_br):
        try:
            d, m, a = data_br.split('/')
            return f"{a}-{m}-{d}"
        except:
            return None

    data_ini_sql = br_to_sql(data_ini) if data_ini else None
    data_fim_sql = br_to_sql(data_fim) if data_fim else None

    # ===============================
    # LANÇAMENTO DIVERSOS
    # ===============================
    if request.method == "POST" and "lancar_diverso" in request.POST:
        try:
            unidade = request.POST.get('unidade_id')
            tipo = request.POST.get('tipo')
            categoria = request.POST.get('categoria')
            descricao = request.POST.get('descricao')
            valor = float(request.POST.get('valor') or 0)
            
            # ✅ REGISTRO DEFINITIVO: Captura o username no momento do clique
            usuario_nome = request.user.username if request.user.is_authenticated else "sistema"

            if not unidade:
                raise Exception("Selecione a unidade")
            if valor <= 0:
                raise Exception("Valor inválido")
            if tipo == "Saída":
                valor = -abs(valor)

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO caixa
                    (paciente_nome, profissional_nome, valor, forma_pagamento,
                     status, categoria, descricao, data_pagamento, unidade_id, usuario_lancamento)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE,%s,%s)
                """, ["-", "-", valor, tipo, "Pago", categoria or "Diversos", descricao, unidade, usuario_nome])

            mensagem = '<div class="alert alert-success">✅ Lançamento realizado com sucesso!</div>'

        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ {e}</div>'

    # ===============================
    # UNIDADES E CATEGORIAS
    # ===============================
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome FROM unidades ORDER BY nome")
        unidades_list = cursor.fetchall()
        cursor.execute("""
            SELECT DISTINCT categoria 
            FROM caixa 
            WHERE paciente_nome = '-' 
            ORDER BY categoria
        """)
        categorias_list = [c[0] for c in cursor.fetchall() if c[0]]

    # ===============================
    # SQL PRINCIPAL
    # ===============================
    sql = """
        SELECT categoria, paciente_nome, profissional_nome, valor, 
               forma_pagamento, status, data_pagamento, unidade_id, descricao, usuario_lancamento
        FROM caixa
        WHERE 1=1
    """
    params = []
    if data_ini_sql:
        sql += " AND data_pagamento::date >= %s"
        params.append(data_ini_sql)
    if data_fim_sql:
        sql += " AND data_pagamento::date <= %s"
        params.append(data_fim_sql)
    if not data_ini_sql and not data_fim_sql:
        sql += " AND data_pagamento::date = %s"
        params.append(hoje)
    if unidade_id:
        sql += " AND unidade_id = %s"
        params.append(unidade_id)
    if busca:
        sql += """
        AND (
            paciente_nome ILIKE %s OR
            profissional_nome ILIKE %s OR
            descricao ILIKE %s OR
            categoria ILIKE %s OR
            usuario_lancamento ILIKE %s
        )
        """
        params.extend([f"%{busca}%"] * 5)

    sql += " ORDER BY data_pagamento DESC, id DESC"

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        movimentos = cursor.fetchall()

    # ===============================
    # BLOCOS E SOMAS
    # ===============================
    total_consultas = total_exames = total_odonto = total_faturado = total_diversos = total_retorno = 0
    pix_total = cartao_total = dinheiro_total = 0
    linhas_consultas = linhas_exames = linhas_odonto = linhas_faturado = linhas_diversos = linhas_retorno = ""

    # ✅ Captura o usuário atual para preencher caso o banco esteja vazio
    user_atual = request.user.username if request.user.is_authenticated else "S.I"

    for m in movimentos:
        cat, pac, prof, val, forma, status, data_pg, uni, desc, user_nome_db = m
        val = float(val or 0)
        pac = limpar_nome(pac)
        data_br = data_pg.strftime('%d/%m/%Y') if data_pg else ""
        descricao = (desc or "").strip()
        
        # ✅ CORREÇÃO: Se não houver usuário no banco, exibe o usuário logado (S.I como fallback)
        user_display = user_nome_db if (user_nome_db and str(user_nome_db).strip() != "" and str(user_nome_db) != "None") else user_atual

        linha_html = f"<tr><td>{data_br}</td><td>{pac}</td><td class='small text-primary font-weight-bold'>{user_display}</td><td>{prof or '-'}</td><td>{descricao}</td><td>R$ {val:.2f}</td><td>{forma}</td></tr>"

        if "retorno" in descricao.lower():
            total_retorno += val; linhas_retorno += linha_html
        elif status == "Pago" and cat not in ["Exame", "Odonto", "Odontologia"] and pac != "-":
            total_consultas += val; linhas_consultas += linha_html
        elif status == "Pago" and cat == "Exame":
            total_exames += val; linhas_exames += linha_html
        elif status == "Pago" and cat in ["Odonto", "Odontologia"]:
            total_odonto += val; linhas_odonto += linha_html
        elif pac == "-":
            total_diversos += val
            linhas_diversos += f"<tr><td>{data_br}</td><td>{descricao}</td><td class='small text-primary font-weight-bold'>{user_display}</td><td>{cat}</td><td>{forma}</td><td>R$ {val:.2f}</td></tr>"
        else:
            total_faturado += val; linhas_faturado += linha_html.replace(f"<td>{forma}</td>", "<td>Faturado</td>")

        if forma.lower() == "pix": pix_total += val
        elif forma.lower() in ["cartão", "cartao"]: cartao_total += val
        elif forma.lower() == "dinheiro": dinheiro_total += val

    total_geral = total_consultas + total_exames + total_odonto + total_faturado + total_diversos + total_retorno

    # ===============================
    # HTML FINAL
    # ===============================
    opts_uni = "".join([f'<option value="{u[0]}" {"selected" if str(unidade_id)==str(u[0]) else ""}>{u[1]}</option>' for u in unidades_list])
    opts_cat = "".join([f'<option value="{c}">{c}</option>' for c in categorias_list])
    cabecalho_tab = "<tr><th>Data</th><th>Paciente</th><th>Usuário</th><th>Profissional</th><th>Descrição</th><th>Valor</th><th>Forma</th></tr>"

    conteudo = f"""
    <div class="container-fluid">
    <h5 class="fw-bold text-success">💰 Caixa Geral</h5>
    {mensagem}
    <form method="GET" class="row g-2 mb-3">
        <div class="col-md-2"><input type="text" name="data_ini" value="{data_ini}" class="form-control" placeholder="Início DD/MM/AAAA"></div>
        <div class="col-md-2"><input type="text" name="data_fim" value="{data_fim}" class="form-control" placeholder="Fim DD/MM/AAAA"></div>
        <div class="col-md-3"><input type="text" name="busca" value="{busca}" class="form-control" placeholder="Buscar por Paciente, Usuário ou Descrição..."></div>
        <div class="col-md-3"><select name="unidade" class="form-select"><option value="">Todas Unidades</option>{opts_uni}</select></div>
        <div class="col-md-2"><button class="btn btn-primary w-100">Filtrar</button></div>
    </form>

    <div class="card p-3 mb-4 border-dark bg-light shadow-sm">
        <h6 class="fw-bold"><i class="bi bi-plus-circle"></i> Caixa Diversos (Entradas/Saídas Manuais)</h6>
        <form method="POST" class="row g-2">
            <div class="col-md-2"><select name="unidade_id" class="form-select" required><option value="">Unidade</option>{opts_uni}</select></div>
            <div class="col-md-2"><select name="tipo" class="form-select"><option>Entrada</option><option>Saída</option></select></div>
            <div class="col-md-2"><input list="lista_categorias" name="categoria" class="form-control" placeholder="Categoria"><datalist id="lista_categorias">{opts_cat}</datalist></div>
            <div class="col-md-3"><input type="text" name="descricao" class="form-control" placeholder="Descrição"></div>
            <div class="col-md-2"><input type="number" step="0.01" name="valor" class="form-control" placeholder="Valor R$"></div>
            <div class="col-md-1"><button name="lancar_diverso" class="btn btn-dark w-100">OK</button></div>
        </form>
    </div>

    <div class="card mb-3 border-success shadow-sm">
        <div class="card-header bg-success text-white fw-bold">Consultas Particulares - Total: R$ {total_consultas:.2f}</div>
        <div class="table-responsive"><table class="table table-sm table-hover">{cabecalho_tab}{linhas_consultas or '<tr><td colspan="7" class="text-center">Sem registros</td></tr>'}</table></div>
    </div>

    <div class="card mb-3 border-warning shadow-sm">
        <div class="card-header bg-warning fw-bold">Convênios / Faturados - Total: R$ {total_faturado:.2f}</div>
        <div class="table-responsive"><table class="table table-sm table-hover">{cabecalho_tab.replace('Valor', 'Status')}{linhas_faturado or '<tr><td colspan="7" class="text-center">Sem registros</td></tr>'}</table></div>
    </div>

    <div class="card mb-3 border-info shadow-sm">
        <div class="card-header bg-info text-white fw-bold">Retornos - Total: R$ {total_retorno:.2f}</div>
        <div class="table-responsive"><table class="table table-sm table-hover">{cabecalho_tab}{linhas_retorno or '<tr><td colspan="7" class="text-center">Sem registros</td></tr>'}</table></div>
    </div>

    <div class="card mb-3 border-primary shadow-sm">
        <div class="card-header bg-primary text-white fw-bold">Exames - Total: R$ {total_exames:.2f}</div>
        <div class="table-responsive"><table class="table table-sm table-hover">{cabecalho_tab}{linhas_exames or '<tr><td colspan="7" class="text-center">Sem registros</td></tr>'}</table></div>
    </div>

    <div class="card mb-3 border-dark shadow-sm">
        <div class="card-header bg-dark text-white fw-bold">Odontologia - Total: R$ {total_odonto:.2f}</div>
        <div class="table-responsive"><table class="table table-sm table-hover">{cabecalho_tab}{linhas_odonto or '<tr><td colspan="7" class="text-center">Sem registros</td></tr>'}</table></div>
    </div>

    <div class="card mb-3 border-secondary shadow-sm">
        <div class="card-header bg-secondary text-white fw-bold">Caixa Diversos / Despesas - Total: R$ {total_diversos:.2f}</div>
        <div class="table-responsive">
            <table class="table table-sm table-hover">
                <thead class="table-light"><tr><th>Data</th><th>Descrição</th><th>Usuário</th><th>Categoria</th><th>Tipo</th><th>Valor</th></tr></thead>
                <tbody>{linhas_diversos or '<tr><td colspan="6" class="text-center">Sem registros</td></tr>'}</tbody>
            </table>
        </div>
    </div>

    <div class="card mt-3 p-3 bg-dark text-white shadow">
        <div class="row text-center align-items-center">
            <div class="col-md-3 border-end"><h5>Total Geral: R$ {total_geral:.2f}</h5></div>
            <div class="col-md-3">Pix: R$ {pix_total:.2f}</div>
            <div class="col-md-3">Cartão: R$ {cartao_total:.2f}</div>
            <div class="col-md-3">Dinheiro: R$ {dinheiro_total:.2f}</div>
        </div>
    </div>
    </div>
    """
    return HttpResponse(base_html("Caixa", conteudo))









# --- CONFIGURAÇÃO DE ROTAS DO SISTEMA SEMPRE VIDA ---

# --- CONFIGURAÇÃO DE ROTAS DO SISTEMA SEMPRE VIDA ---
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
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   

   
]
