from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# --- TEMPLATE BASE (DESIGN SEMPRE VIDA) ---
def base_html(titulo, conteudo):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>{titulo} - Sempre Vida</title>
        <style>
            body {{ background-color: #f0f2f5; padding: 15px; font-family: 'Segoe UI', sans-serif; }}
            .card-box {{ max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }}
            .btn-save {{ padding: 15px; font-size: 1.1rem; font-weight: bold; border-radius: 10px; }}
            .unidade-item {{ border-bottom: 1px solid #eee; padding: 15px 0; }}
            .unidade-nome {{ font-size: 1.1rem; font-weight: bold; color: #2c3e50; display: block; }}
            .unidade-info {{ font-size: 0.9rem; color: #6c757d; margin-top: 5px; }}
        </style>
    </head>
    <body>
        <div class="card-box">
            {conteudo}
        </div>
    </body>
    </html>
    """

# --- TELA 1: CADASTRO / EDIÇÃO DE UNIDADE ---
@csrf_exempt
def cadastro_unidade(request):
    mensagem = ""
    edit_id = request.GET.get('edit')
    unidade_dados = {"id": "", "nome": "", "endereco": "", "telefone": ""}

    # Se estiver editando, busca os dados atuais
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome, endereco, telefone FROM unidades WHERE id = %s", [edit_id])
            row = cursor.fetchone()
            if row:
                unidade_dados = {"id": row[0], "nome": row[1], "endereco": row[2], "telefone": row[3]}

    if request.method == "POST":
        id_post = request.POST.get('id')
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        telefone = request.POST.get('telefone')
        
        try:
            with connection.cursor() as cursor:
                if id_post: # Atualiza se já existir ID
                    cursor.execute(
                        "UPDATE unidades SET nome=%s, endereco=%s, telefone=%s WHERE id=%s",
                        [nome, endereco, telefone, id_post]
                    )
                    mensagem = '<div class="alert alert-success">✅ Unidade Atualizada!</div>'
                else: # Cria novo se não tiver ID
                    cursor.execute(
                        "INSERT INTO unidades (nome, endereco, telefone) VALUES (%s, %s, %s)", 
                        [nome, endereco, telefone]
                    )
                    mensagem = '<div class="alert alert-success">✅ Unidade Cadastrada!</div>'
        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ Erro: {e}</div>'

    conteudo = f"""
        <div class="text-center mb-4">
            <span style="font-size: 40px;">🏢</span>
            <h2 class="mt-2">{"Editar Unidade" if edit_id else "Nova Unidade"}</h2>
        </div>
        {mensagem}
        <form method="POST">
            <input type="hidden" name="id" value="{unidade_dados['id']}">
            <div class="mb-3">
                <label class="form-label fw-bold">Nome da Unidade</label>
                <input type="text" name="nome" class="form-control form-control-lg" value="{unidade_dados['nome']}" required>
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Endereço Completo</label>
                <input type="text" name="endereco" class="form-control form-control-lg" value="{unidade_dados['endereco']}">
            </div>
            <div class="mb-3">
                <label class="form-label fw-bold">Telefone</label>
                <input type="tel" name="telefone" class="form-control form-control-lg" value="{unidade_dados['telefone']}">
            </div>
            <button type="submit" class="btn btn-success w-100 btn-save mt-3 shadow-sm">Salvar Unidade</button>
        </form>
        <div class="text-center mt-4">
            <a href="/unidades/lista/" class="text-decoration-none text-primary fw-bold">📋 Ver Unidades Ativas</a>
        </div>
    """
    return HttpResponse(base_html("Cadastro Unidade", conteudo))

# --- TELA 2: LISTAGEM COM BOTÃO VOLTAR ---
def lista_unidades(request):
    # Lógica de Exclusão
    delete_id = request.GET.get('delete')
    if delete_id:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM unidades WHERE id = %s", [delete_id])
        return HttpResponseRedirect('/unidades/lista/')

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome, endereco, telefone FROM unidades ORDER BY nome ASC")
            unidades = cursor.fetchall()
        
        itens = ""
        for u in unidades:
            itens += f"""
            <div class="unidade-item">
                <div class="d-flex justify-content-between align-items-start">
                    <div style="flex: 1;">
                        <span class="unidade-nome">{u[1]}</span>
                        <div class="unidade-info">📍 {u[2] if u[2] else 'Sem endereço'}</div>
                        <div class="unidade-info">📞 {u[3] if u[3] else 'Sem telefone'}</div>
                    </div>
                    <div class="d-flex gap-2">
                        <a href="/?edit={u[0]}" class="btn btn-sm btn-outline-warning">Editar</a>
                        <a href="/unidades/lista/?delete={u[0]}" class="btn btn-sm btn-outline-danger" onclick="return confirm('Excluir unidade?')">Excluir</a>
                    </div>
                </div>
            </div>"""

        conteudo = f"""
            <h3 class="mb-4 text-center">📋 Unidades Ativas</h3>
            <div style="min-height: 200px;">
                {itens if unidades else '<p class="text-center text-muted">Nenhuma unidade cadastrada.</p>'}
            </div>
            <div class="mt-4 d-grid gap-2">
                <a href="/" class="btn btn-primary btn-save shadow-sm">➕ Nova Unidade</a>
                <a href="/" class="btn btn-outline-secondary py-2 fw-bold">⬅️ Voltar</a>
            </div>
        """
        return HttpResponse(base_html("Lista de Unidades", conteudo))
    except Exception as e:
        return HttpResponse(f"Erro: {e}")

# --- ROTAS ---
urlpatterns = [
    path('', cadastro_unidade),
    path('unidades/lista/', lista_unidades),
]
