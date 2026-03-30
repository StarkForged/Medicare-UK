import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicare_uk.settings')
application = get_wsgi_application()
