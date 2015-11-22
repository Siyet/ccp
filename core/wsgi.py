import os
import sys
import site

sys.path.append('/var/www/cloud/data/www/network.itex.su')

site.addsitedir('/var/virtualenvs/itex_network/lib/python2.7/site-packages')

activate_this = os.path.expanduser("/var/virtualenvs/itex_network/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.prod")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
