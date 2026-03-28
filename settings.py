import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = 'django-insecure-sua-chave-aqui' # Depois trocamos por uma segura
DEBUG = True
ALLOWED_HOSTS = ['*'] # Permite que a Railway rode o site

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Removi o 'app' daqui
]

# Configuração simples de Banco de Dados (SQLite por enquanto, depois Supabase)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
STATIC_URL = 'static/'







import os

# Procure a lista de MIDDLEWARE e adicione esta linha no topo dela:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Adicione esta se quiser carregar imagens/estilos
    # ... as outras que já estão lá ...
]

# No final do arquivo, adicione isso para a Railway não te bloquear:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
