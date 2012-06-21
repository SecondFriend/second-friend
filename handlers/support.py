from handlers import AbstractHandler

from models import Configo, Counselor
from google.appengine.api import users

import logging
import settings

class Support(AbstractHandler):
    def get(self):        
        counselor = Counselor.get_or_insert(str(users.get_current_user().user_id()))
        if not counselor.name:
            counselor.name = users.get_current_user().nickname()
            counselor.put()

        logging.info(str(counselor.key().id()))
        template_vars = {
            'app_name': settings.APP_NAME,
            'counselor': counselor,
            'logout_url': '/logout',
            'where': 'Support'
        }

        self._output_template('support.html', **template_vars)