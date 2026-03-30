from django.urls import path
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- FUNÇÃO: CADASTRO DE UNIDADES ---
@csrf_exempt
def cadastro_unidade(request):
    mensagem = ""
    if request.method == "POST":
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        telefone = request.POST.get('telefone')

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO unidades (nome, endereco, telefone) VALUES (%s, %s, %s)",
                    [nome, endereco, telefone]
                )
            mensagem = '<div class="alert alert-success">✅ Unidade Cadastrada com Sucesso!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>Unidades - Sempre Vida</title>
    </head>
    <body class="bg-light p-3">
        <div class="container bg-white p-4 rounded shadow-sm" style="max-width: 500px;">
            <h3 class="text-center mb-4">🏢 Cadastro de Unidade</h3>
            {mensagem}
            <form method="POST">
                <div class="mb-3"><label class="form-label fw-bold">Nome da Unidade</label><input type="text" name="nome" class="form-control" required placeholder="Ex: Unidade Centro"></div>
                <div class="mb-3"><label class="form-label">Endereço</label><input type="text" name="endereco" class="form-control"></div>
                <div class="mb-3"><label class="form-label">Telefone</label><input type="text" name="telefone" class="form-control"></div>
                <button type="submit" class="btn btn-success w-100 mb-2">Salvar Unidade</button>
                <a href="/unidades/lista" class="btn btn-outline-secondary w-100">📋 Listar Unidades</a>
            </form>
            <hr>
            <a href="/" class="btn btn-link w-100">Voltar ao Início</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

# --- FUNÇÃO: LISTAGEM DE UNIDADES (COM EDITAR/EXCLUIR) ---
def lista_unidades(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome, endereco, telefone FROM unidades ORDER BY nome ASC")
            unidades = cursor.fetchall()
        
        linhas = ""
        for u in unidades:
            linhas += f"""
            <tr>
                <td>{u[1]}</td>
                <td>{u[3]}</td>
                <td>
                    <button class="btn btn-sm btn-warning">Editar</button>
                    <button class="btn btn-sm btn-danger">Excluir</button>
                </td>
            </tr>"""

        html = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <title>Lista de Unidades</title>
        </head>
        <body class="bg-light p-3">
            <div class="container bg-white p-4 rounded shadow-sm">
                <h3 class="mb-4">📋 Unidades Cadastradas</h3>
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-dark"><tr><th>Nome</th><th>Telefone</th><th>Ações</th></tr></thead>
                        <tbody>{linhas}</tbody>
                    </table>
                </div>
                <a href="/unidades" class="btn btn-primary">Nova Unidade</a>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"Erro: {e}")

# --- URLS ANTERIORES E NOVAS ---
urlpatterns = [
    # Manter as rotas de pacientes que já funcionam
    path('unidades/', cadastro_unidade),
    path('unidades/lista/', lista_unidades),
]
