from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime
import re
import urllib.parse
from django.db import connection

# --- TELA 16: CAIXA COMPLETO + GUIA EXAME ---
@csrf_exempt
def caixa_geral(request):
    hoje = datetime.date.today()
    unidade_id = request.GET.get('unidade') or ""
    data_ini = request.GET.get('data_ini') or ""
    data_fim = request.GET.get('data_fim') or ""
    busca = request.GET.get('busca') or ""
    mensagem = ""

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

    # LANÇAMENTO DIVERSOS
    if request.method == "POST" and "lancar_diverso" in request.POST:
        try:
            unidade = request.POST.get('unidade_id')
            tipo = request.POST.get('tipo')
            categoria = request.POST.get('categoria')
            descricao = request.POST.get('descricao')
            valor = float(request.POST.get('valor') or 0)

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
                     status, categoria, descricao, data_pagamento, unidade_id)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE,%s)
                """, ["-", "-", valor, tipo, "Pago", categoria or "Diversos", descricao, unidade])

            mensagem = '<div class="alert alert-success">✅ Lançamento realizado!</div>'

        except Exception as e:
            mensagem = f'<div class="alert alert-danger">❌ {e}</div>'

    # UNIDADES
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

    # SQL PRINCIPAL
    sql = """
        SELECT categoria, paciente_nome, profissional_nome, valor, 
               forma_pagamento, status, data_pagamento, unidade_id, descricao
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
            categoria ILIKE %s
        )
        """
        params.extend([f"%{busca}%"] * 4)

    sql += " ORDER BY data_pagamento DESC, id DESC"

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        movimentos = cursor.fetchall()

    # BLOCOS E SOMAS
    total_consultas = total_exames = total_odonto = total_faturado = total_diversos = total_retorno = 0
    pix_total = cartao_total = dinheiro_total = 0
    linhas_consultas = linhas_exames = linhas_odonto = linhas_faturado = linhas_diversos = linhas_retorno = ""

    for m in movimentos:
        cat, pac, prof, val, forma, status, data_pg, uni, desc = m
        val = float(val or 0)
        pac = limpar_nome(pac)
        data_br = data_pg.strftime('%d/%m/%Y') if data_pg else ""
        descricao = (desc or "").strip()

        # BOTÃO GERAR GUIA
        btn_guia = ""
        if cat == "Exame" and pac != "-":
            params_pdf = urllib.parse.urlencode({
                "paciente": pac,
                "exame": descricao,
                "prestador": prof or "-",
                "data": data_br
            })
            btn_guia = f'<a href="/gerar_guia_pdf/?{params_pdf}" target="_blank" class="btn btn-sm btn-primary">Gerar Guia</a>'

        if "retorno" in descricao.lower():
            total_retorno += val
            linhas_retorno += f"<tr><td>{data_br}</td><td>{pac}</td><td>{prof or '-'}</td><td>{descricao}</td><td>R$ {val:.2f}</td><td>{forma}</td></tr>"
        elif status == "Pago" and cat not in ["Exame", "Odonto", "Odontologia"] and pac != "-":
            total_consultas += val
            linhas_consultas += f"<tr><td>{data_br}</td><td>{pac}</td><td>{prof or '-'}</td><td>{descricao}</td><td>R$ {val:.2f}</td><td>{forma}</td></tr>"
        elif status == "Pago" and cat == "Exame":
            total_exames += val
            linhas_exames += f"<tr><td>{data_br}</td><td>{pac} {btn_guia}</td><td>{prof or '-'}</td><td>{descricao}</td><td>R$ {val:.2f}</td><td>{forma}</td></tr>"
        elif status == "Pago" and cat in ["Odonto", "Odontologia"]:
            total_odonto += val
            linhas_odonto += f"<tr><td>{data_br}</td><td>{pac}</td><td>{prof or '-'}</td><td>{descricao}</td><td>R$ {val:.2f}</td><td>{forma}</td></tr>"
        elif pac == "-":
            total_diversos += val
            linhas_diversos += f"<tr><td>{data_br}</td><td>{descricao}</td><td>{cat}</td><td>{forma}</td><td>R$ {val:.2f}</td></tr>"
        else:
            total_faturado += val
            linhas_faturado += f"<tr><td>{data_br}</td><td>{pac}</td><td>{prof or '-'}</td><td>{descricao}</td><td>Faturado</td></tr>"

        if forma.lower() == "pix":
            pix_total += val
        elif forma.lower() in ["cartão", "cartao"]:
            cartao_total += val
        elif forma.lower() == "dinheiro":
            dinheiro_total += val

    total_geral = total_consultas + total_exames + total_odonto + total_faturado + total_diversos + total_retorno

    # SELECTS
    opts_uni = "".join([f'<option value="{u[0]}" {"selected" if str(unidade_id)==str(u[0]) else ""}>{u[1]}</option>' for u in unidades_list])
    opts_cat = "".join([f'<option value="{c}">{c}</option>' for c in categorias_list])

    conteudo = f"""
    <div class="container-fluid">
        <h5 class="fw-bold text-success">💰 Caixa Geral</h5>
        {mensagem}

        <!-- FILTROS -->
        <form method="GET" class="row g-2 mb-3">
            <div class="col-md-2"><input type="text" name="data_ini" value="{data_ini}" class="form-control" placeholder="Data Inicial"></div>
            <div class="col-md-2"><input type="text" name="data_fim" value="{data_fim}" class="form-control" placeholder="Data Final"></div>
            <div class="col-md-3"><input type="text" name="busca" value="{busca}" class="form-control" placeholder="Buscar..."></div>
            <div class="col-md-3"><select name="unidade" class="form-select"><option value="">Todas</option>{opts_uni}</select></div>
            <div class="col-md-2"><button class="btn btn-primary w-100">Filtrar</button></div>
        </form>

        <!-- FORM DIVERSOS -->
        <div class="card p-3 mb-3 border-dark">
            <h5>➕ Caixa Diversos</h5>
            <form method="POST" class="row g-2">
                <div class="col-md-2"><select name="unidade_id" class="form-select" required><option value="">Unidade</option>{opts_uni}</select></div>
                <div class="col-md-2"><select name="tipo" class="form-select"><option>Entrada</option><option>Saída</option></select></div>
                <div class="col-md-2"><input list="lista_categorias" name="categoria" class="form-control" placeholder="Categoria"><datalist id="lista_categorias">{opts_cat}</datalist></div>
                <div class="col-md-3"><input type="text" name="descricao" class="form-control" placeholder="Descrição"></div>
                <div class="col-md-2"><input type="number" step="0.01" name="valor" class="form-control" placeholder="Valor"></div>
                <div class="col-md-1"><button name="lancar_diverso" class="btn btn-dark w-100">OK</button></div>
            </form>
        </div>

        <!-- BLOCOS -->
        <div class="card mb-3">
            <div class="card-header bg-success text-white">Consultas - Total: R$ {total_consultas:.2f}</div>
            <table class="table">{linhas_consultas or '<tr><td colspan="6" class="text-center">Sem registros</td></tr>'}</table>
        </div>

        <div class="card mb-3">
            <div class="card-header bg-warning">Convênios - Total: R$ {total_faturado:.2f}</div>
            <table class="table">{linhas_faturado or '<tr><td colspan="5" class="text-center">Sem registros</td></tr>'}</table>
        </div>

        <div class="card mb-3">
            <div class="card-header bg-info text-white">Retorno - Total: R$ {total_retorno:.2f}</div>
            <table class="table">{linhas_retorno or '<tr><td colspan="6" class="text-center">Sem registros</td></tr>'}</table>
        </div>

        <div class="card mb-3">
            <div class="card-header bg-primary text-white">Exames - Total: R$ {total_exames:.2f}</div>
            <table class="table">{linhas_exames or '<tr><td colspan="6" class="text-center">Sem registros</td></tr>'}</table>
        </div>

        <div class="card mb-3">
            <div class="card-header bg-dark text-white">Odontologia - Total: R$ {total_odonto:.2f}</div>
            <table class="table">{linhas_odonto or '<tr><td colspan="6" class="text-center">Sem registros</td></tr>'}</table>
        </div>

        <div class="card mb-3">
            <div class="card-header bg-secondary text-white">Diversos - Total: R$ {total_diversos:.2f}</div>
            <table class="table">
                <tr><th>Data</th><th>Descrição</th><th>Categoria</th><th>Tipo</th><th>Valor</th></tr>
                {linhas_diversos or '<tr><td colspan="5" class="text-center">Sem registros</td></tr>'}
            </table>
        </div>

        <!-- TOTAL GERAL -->
        <div class="card mt-3 p-3">
            <h5>Total Geral: R$ {total_geral:.2f}</h5>
            <p>Pix: R$ {pix_total:.2f} | Cartão: R$ {cartao_total:.2f} | Dinheiro: R$ {dinheiro_total:.2f}</p>
        </div>
    </div>
    """

    return HttpResponse(base_html("Caixa", conteudo))


# --- VIEW PARA GERAR GUIA DE EXAME ---
@csrf_exempt
def gerar_guia_pdf(request):
    paciente = request.GET.get('paciente', '-')
    exame = request.GET.get('exame', '-')
    prestador = request.GET.get('prestador', '-')
    data = request.GET.get('data', datetime.date.today().strftime('%d/%m/%Y'))

    conteudo = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Guia de Exame</title>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            h2 {{ text-align: center; color: #2c3e50; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .assinatura {{ margin-top: 50px; }}
            .assinatura div {{ display: inline-block; width: 45%; text-align: center; }}
        </style>
    </head>
    <body>
        <h2>Guia de Exame</h2>
        <table>
            <tr><th>Paciente</th><td>{paciente}</td></tr>
            <tr><th>Exame</th><td>{exame}</td></tr>
            <tr><th>Prestador</th><td>{prestador}</td></tr>
            <tr><th>Data</th><td>{data}</td></tr>
        </table>

        <div class="assinatura">
            <div>
                ___________________________<br>
                Assinatura do Paciente
            </div>
            <div>
                ___________________________<br>
                Assinatura da Clínica
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(conteudo)
