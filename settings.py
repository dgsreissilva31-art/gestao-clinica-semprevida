import os
from pathlib import Path
import dj_database_url

# 1. CAMINHOS BASE
# Define a raiz do projeto para localizar templates e arquivos estáticos
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SEGURANÇA
# Em produção, use uma variável de ambiente para a SECRET_KEY
SECRET_KEY = 'django-insecure-clinica-sempre-vida-final-v2026'

# Debug deve ser False em produção
DEBUG = True

# Permitir todos os hosts (ajuste para o domínio real no deploy)
ALLOWED_HOSTS = ['*']

# 3. DEFINIÇÃO DE APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',           # Essencial para login
    'django.contrib.contenttypes',
    'django.contrib.sessions',       # Essencial para manter o usuário logado
    'django.contrib.messages',
    'django.contrib.staticfiles',    # Essencial para CSS/JS
]

# 4. MIDDLEWARES (ORDEM IMPORTANTE)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    # Para servir arquivos estáticos no deploy
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Essencial para @login_required
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 5. URLS E WSGI
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

# 6. TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth', # Permite usar {{ user }} no HTML
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 7. BANCO DE DADOS (SUPABASE VIA POOLER)
# Usando dj_database_url para converter a string do Supabase automaticamente
DATABASES = {
    'default': dj_database_url.parse(
        'postgresql://postgres.rslaudmbyfcxgtlbowis:fZqMFxZDb0sa5aT3@aws-1-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require',
        conn_max_age=0
    )
}

# 8. VALIDAÇÃO DE SENHAS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 9. INTERNACIONALIZAÇÃO
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# 10. ARQUIVOS ESTÁTICOS (CSS, JS, IMAGES)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuração para o WhiteNoise (Deploy)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 11. PADRÕES DE MODELOS
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 12. CONFIGURAÇÕES DE LOGIN (ESSENCIAL)
# Define para onde o usuário vai se não estiver logado
LOGIN_URL = '/login/'
# Define para onde ele vai após logar com sucesso
LOGIN_REDIRECT_URL = '/admin-painel/'
# Define para onde ele vai após sair do sistema
LOGOUT_REDIRECT_URL = '/login/'

# 13. SEGURANÇA PARA DEPLOY (HTTPS)
# Necessário para Railway e similares que usam proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
