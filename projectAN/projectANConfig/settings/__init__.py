import os

SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')

if not SETTINGS_MODULE or SETTINGS_MODULE == 'projectANConfig.settings':
    from .dev import *
elif SETTINGS_MODULE == 'projectANConfig.settings.prod':
    from .prod import *
elif SETTINGS_MODULE == 'projectANConfig.settings.test':
    from .test import *