import os
from django.core.wsgi import get_wsgi_application

# Define qual arquivo de configurações o servidor deve ler
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()
