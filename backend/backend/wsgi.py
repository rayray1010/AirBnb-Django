"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""


import os
import dotenv
from django.core.wsgi import get_wsgi_application
dotenv.read_dotenv(os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.env'))
print(os.environ.get('DB_NAME'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
