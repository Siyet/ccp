import os
import sys
import site

sys.path.append('/var/www/costumecode')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
