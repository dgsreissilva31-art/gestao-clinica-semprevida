from django.db import connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime, re, urllib.parse
from reportlab.pdfgen import canvas
from io import BytesIO

# ===============================
# VIEW PARA GERAR PDF
# ===============================
def gerar_guia_pdf(request):
    paciente = request.GET.get("paciente", "")
    exame = request.GET.get("exame", "")
    prestador = request.GET.get("prestador", "")
    data = request.GET.get("data", "")
    
    # Criar PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica", 12)
    
    c.drawString(50, 800, "GUIA DE EXAME")
    c.drawString(50, 770, f"Paciente: {paciente}")
    c.drawString(50, 750, f"Exame: {exame}")
    c.drawString(50, 730, f"Prestador: {prestador}")
    c.drawString(50, 710, f"Data: {data}")
    
    c.drawString(50, 680, "Assinatura do paciente: ______________________")
    c.drawString(50, 660, "Assinatura da clínica: _______________________")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=guia_{paciente}.pdf'
    return response

# ===============================
# VIEW PRINCIPAL CAIXA
# ===============================
@csrf_exempt
def caixa_geral(request):
    hoje = datetime.date.today()
    unidade_id = request.GET.get('unidade') or ""
    data_ini = request.GET.get('data_ini') or ""
    data_fim = request.GET.get('data_fim') or ""
    busca = request.GET.get('busca') or ""
    mensagem = ""

    # Funções auxiliares
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

        # BLOCOS
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

    # HTML FINAL
    conteudo = f"""
    <div class="container-fluid">
        <h5 class="fw-bold text-success">💰 Caixa Geral</h5>
        {mensagem}

        <form method="GET" class="row g-2 mb-3">
            <div class="col-md-2"><input type="text" name="data_ini" value="{data_ini}" class="form-control" placeholder="Data Inicial"></div>
            <div class="col-md-2"><input type="text" name="data_fim" value="{data_fim}" class="form-control" placeholder="Data Final"></div>
            <div class="col-md-3"><input type="text" name="busca" value="{busca}" class="form-control" placeholder="Buscar..."></div>
            <div class="col-md-3"><select name="unidade" class="form-select"><option value="">Todas</option>{opts_uni}</select></div>
            <div class="col-md-2"><button class="btn btn-primary w-100">Filtrar</button></div>
        </form>

        <div class="card mb-3">
            <div class="card-header bg-primary text-white">Exames - Total: R$ {total_exames:.2f}</div>
            <table class="table">{linhas_exames or '<tr><td colspan="6" class="text-center">Sem registros</td></tr>'}</table>
        </div>
    </div>
    """

    return HttpResponse(conteudo)
