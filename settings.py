import os
from pathlib import Path
import dj_database_url

# Caminho base do projeto - Ajustado para estrutura simples
BASE_DIR = Path(__file__).resolve().parent

# Chave de segurança
SECRET_KEY = 'django-insecure-chave-clinica-sempre-vida'

# Modo de depuração
DEBUG = True

# Permite que o link da Railway acesse o sistema
ALLOWED_HOSTS = ['*']

# ========================
# APPS
# ========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# ========================
# MIDDLEWARE
# ========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# AJUSTE IMPORTANTE: Se seu arquivo no GitHub for 'urls.py', usamos 'urls'.
# Se estiver dentro de uma pasta 'core', usamos 'core.urls'. 
# Vou deixar 'urls' que é o padrão da sua estrutura anterior.
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

# ========================
# TEMPLATES
# ========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ========================
# 🔥 BANCO DE DADOS (SUPABASE - POOLER CORRIGIDO)
# ========================
# Usando a senha fZqMFxZDb0sa5aT3 que você passou
DATABASES = {
    'default': dj_database_url.parse(
        'postgresql://postgres.rslaudmbyfcxgtlbowis:fZqMFxZDb0sa5aT3@aws-0-sa-east-1.pooler.supabase.com:5432/postgres',
        conn_max_age=600
    )
}

# ========================
# IDIOMA E FUSO
# ========================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ========================
# STATIC (CONFIGURAÇÃO PARA RAILWAY)
# ========================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ========================
# SEGURANÇA E RAILWAY
# ========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
