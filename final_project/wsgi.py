"""
WSGI config for final_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application


# add the hellodjango project path into the sys.path
sys.path.append('/Users/joe/Documents/final_project/final_project/')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/Users/joe/Documents/final_project/final_env/Lib/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final_project.settings")

application = get_wsgi_application()
