import os
import sys
import site

sys.path.append('/var/www/costumecode')

site.addsitedir('/var/virtualenvs/costumecode/lib/python2.7/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.prod")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
