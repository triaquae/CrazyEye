#_*_coding:utf-8_*_

from django.conf import settings

import os
settings.TEMPLATES[0]['DIRS'] += [os.path.join(settings.BASE_DIR, 'kingadmin_old/templates')]

settings.STATICFILES_DIRS +=[ os.path.join(settings.BASE_DIR, 'kingadmin_old/statics')]

# print(settings.STATICFILES_DIRS)
# print(settings.TEMPLATES[0]['DIRS'] )