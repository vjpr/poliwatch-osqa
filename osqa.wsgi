import os
import sys
sys.path.append('/home/finsoc/webapps/poliwatch_server')
sys.path.append('/home/finsoc/webapps/poliwatch_server/osqa')
os.environ['DJANGO_SETTINGS_MODULE'] = 'osqa.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
