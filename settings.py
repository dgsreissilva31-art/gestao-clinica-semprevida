import os
from pathlib import Path
import dj_database_url

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent

# Chave de segurança
SECRET_KEY = 'django-insecure-clinica-sempre-vida-v3'

# Modo de depuração (Ativo para diagnóstico)
DEBUG = True

# Permite que a Railway acesse o sistema
ALLOWED_HOSTS = ['*']

# ========================
# APPS E MIDDLEWARE
# ========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

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

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

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
# 🔥 BANCO DE DADOS (CONFIGURAÇÃO DE ALTA COMPATIBILIDADE)
# ========================
# Mudamos para o formato de usuário que o Supabase exige no modo Transaction
DATABASES = {
    'default': dj_database_url.parse(
        'postgresql://postgres.rslaudmbyfcxgtlbowis:fZqMFxZDb0sa5aT3@aws-0-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require',
        conn_max_age=0  # Pooler prefere conexões curtas
    )
}

# ========================
# CONFIGURAÇÕES GERAIS
# ========================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
