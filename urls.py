from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- ATUALIZAÇÃO DO TEMPLATE BASE (MENU LATERAL) ---
# Altere apenas a parte da <div class="sidebar"> dentro da sua função base_html:

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

# --- ATUALIZAÇÃO DA TELA 0: PAINEL DE GESTÃO ---
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
        </div>
    """
    return HttpResponse(base_html("Dashboard", conteudo))



# --- UNIDADES (CADASTRO) ---
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

# --- UNIDADES (LISTA COM CONFIRMAÇÃO) ---
def lista_unidades(request):
    if request.GET.get('delete'):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM unidades WHERE id = %s", [request.GET.get('delete')])
        return HttpResponseRedirect('/unidades/lista/')
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, endereco FROM unidades ORDER BY nome")
        unidades = cursor.fetchall()

    linhas = "".join([f'<tr><td>{u[1]}</td><td>{u[2]}</td><td><a href="/unidades/lista/?delete={u[0]}" class="btn btn-sm btn-danger" onclick="return confirm(\'Deseja realmente excluir esta unidade?\')"><i class="bi bi-trash"></i></a></td></tr>' for u in unidades])
    
    conteudo = f"""
        <h4><i class="bi bi-list"></i> Unidades Ativas</h4><hr>
        <table class="table table-hover">
            <thead class="table-light"><tr><th>Nome</th><th>Endereço</th><th>Ação</th></tr></thead>
            <tbody>{linhas if unidades else '<tr><td colspan="3">Vazio</td></tr>'}</tbody>
        </table>
        <a href="/unidades/" class="btn btn-primary">Adicionar Nova</a>
    """
    return HttpResponse(base_html("Lista Unidades", conteudo))

# --- ESPECIALIDADES (COM CONFIRMAÇÃO) ---
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

    itens = "".join([f'<tr><td>{d[1]}</td><td>{d[2]}</td><td><a href="/especialidades/?delete_esp={d[0]}" class="btn btn-sm btn-danger" onclick="return confirm(\'Deseja excluir esta especialidade?\')"><i class="bi bi-trash"></i></a></td></tr>' for d in dados])

    conteudo = f"""
        <h4><i class="bi bi-hospital"></i> Especialidades</h4><hr>
        <form method="POST" class="row g-2 mb-4">
            <div class="col-md-6"><input type="text" name="nome" class="form-control" placeholder="Especialidade" required></div>
            <div class="col-md-4"><select name="tipo" class="form-select"><option value="Médica">Médica</option><option value="Odontológica">Odontológica</option></select></div>
            <div class="col-md-2"><button type="submit" class="btn btn-primary w-100">Salvar</button></div>
        </form>
        <table class="table table-sm table-hover">
            <thead><tr><th>Nome</th><th>Tipo</th><th>Ação</th></tr></thead>
            <tbody>{itens if dados else '<tr><td colspan="3">Nenhuma cadastrada.</td></tr>'}</tbody>
        </table>
    """
    return HttpResponse(base_html("Especialidades", conteudo))

urlpatterns = [
    path('', painel_controle),
    path('unidades/', cadastro_unidade),
    path('unidades/lista/', lista_unidades),
    path('especialidades/', especialidades_geral),
]
