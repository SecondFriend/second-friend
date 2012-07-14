from handlers import AbstractHandler

from models import Counselor
from google.appengine.api import users

import settings

class Index(AbstractHandler):
    def get(self):

        # keep non-admin users away
        if not users.is_current_user_admin():
            self.redirect('/')
            
        # if user is an admin
        # render support page    
        if users.is_current_user_admin():

            # get counselor, if new, then insert
            counselor = Counselor.get_or_insert(str(users.get_current_user().user_id()))
        
            # set default counselor name to user's nickname
            if not counselor.name:
                counselor.name = users.get_current_user().nickname() 

            # update user status to 1 - ready for work!
            counselor.status = 1
            counselor.put()

            template_vars = {
                'app_name': settings.APP_NAME,
                'counselor': counselor,
                'logout_url': '/logout',
                'where': 'Support'
            }

            self._output_template('support.html', **template_vars)