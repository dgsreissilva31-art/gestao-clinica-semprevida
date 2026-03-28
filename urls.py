from django.urls import path
from django.http import HttpResponse

def formulario_paciente(request):
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <title>Cadastro - Clínica Sempre Vida</title>
        <style>
            body { background-color: #f8f9fa; }
            .container { max-width: 500px; margin-top: 50px; background: white; padding: 30px; border-radius: 15px; shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .btn-primary { background-color: #007bff; border: none; }
        </style>
    </head>
    <body>
        <div class="container shadow">
            <h2 class="text-center mb-4">🩺 Cadastro de Paciente</h2>
            <form>
                <div class="mb-3">
                    <label class="form-label">Nome Completo</label>
                    <input type="text" class="form-control" placeholder="Ex: João Silva">
                </div>
                <div class="mb-3">
                    <label class="form-label">WhatsApp</label>
                    <input type="tel" class="form-control" placeholder="(00) 00000-0000">
                </div>
                <div class="mb-3">
                    <label class="form-label">Data da Consulta</label>
                    <input type="date" class="form-control">
                </div>
                <div class="mb-3">
                    <label class="form-label">Observações Médicas</label>
                    <textarea class="form-control" rows="3"></textarea>
                </div>
                <button type="button" class="btn btn-primary w-100" onclick="alert('Sistema IA.naEmpresa: Dados capturados!')">Salvar Agendamento</button>
            </form>
            <hr>
            <p class="text-center text-muted small">Consultoria IA.naEmpresa &copy; 2026</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', formulario_paciente),
]
