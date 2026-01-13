"""
WSGI config for library_demo project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_demo.settings')

application = get_wsgi_application()
