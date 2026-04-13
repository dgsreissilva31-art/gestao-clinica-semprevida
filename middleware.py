from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de URLs que podem ser acessadas SEM login
        # Adicionamos '/agendar/' aqui
        urls_abertas = ['/login/', '/agendar/']
        
        # Verifica se a URL atual começa com alguma das URLs abertas
        pode_acessar = any(request.path.startswith(url) for url in urls_abertas)

        if not request.user.is_authenticated and not pode_acessar:
            return redirect('/login/')

        response = self.get_response(request)
        return response
