from settings import BASE_DIR

import gettext
import os


localdir = os.path.join(BASE_DIR, 'locales')
translate = gettext.translation('ru', localdir, ['ru'])
_ = translate.gettext


print(_('Hello'))



