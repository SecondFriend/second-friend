from handlers import AbstractHandler

from models import Counselor
from google.appengine.api import users

import settings

class Index(AbstractHandler):
    def get(self):
        
        # if user is not logged in yet
        # show the welcome page
        if not users.get_current_user():
            # welcome page
            template_vars = {'where': 'Index', 'login_url': '/login'}
            self._output_template('welcome.html', **template_vars)
            return

        # user is logged in but not an admin
        # show the unauthorized page
        if not users.is_current_user_admin():
            # unauthorized page
            template_vars = {'where': 'Administration', 'email': users.get_current_user().email(), 'logout_url': '/logout', }
            self._output_template('unauthorized.html', **template_vars)
            return
            
        # user is an admin - redirect to support page
        # render support page    
        if users.is_current_user_admin():

            self.redirect('/support')

            # get counselor, if new, then insert
            counselor = Counselor.get_or_insert(str(users.get_current_user().user_id()))
        
            # set default counselor name
            if not counselor.name:
                counselor.name = users.get_current_user().nickname()

            # update user status to 1
            counselor.status = 1
            counselor.put()

            template_vars = {
                'app_name': settings.APP_NAME,
                'counselor': counselor,
                'logout_url': '/logout',
                'where': 'Support'
            }

            self._output_template('support.html', **template_vars)
                
class Login(AbstractHandler):

    def get(self):
        # redirect to google login page
        self.redirect(users.create_login_url('/'))
        
class Logout(AbstractHandler):

    def get(self):
        # update user status to 0
        counselor = Counselor.get_by_key_name(str(users.get_current_user().user_id()))
        
        # set status to 0, unavailable
        if counselor:
            counselor.status = 0
            counselor.put()
        
        self.redirect(users.create_logout_url('/'))  