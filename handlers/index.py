from handlers import AbstractHandler

from models import Counselor
from google.appengine.api import users

class Index(AbstractHandler):
    def get(self):
        
        # if user is not logged in yet
        if not users.get_current_user():
            # welcome page
            template_vars = {'where': 'Index', 'login_url': '/login'}
            self._output_template('welcome.html', **template_vars)
            return

        # user is logged in but not an admin
        if not users.is_current_user_admin():
            # unauthorized page
            template_vars = {'where': 'Administration', 'email': users.get_current_user().email(), 'logout_url': '/logout', }
            self._output_template('unauthorized.html', **template_vars)
            return
            
        if users.is_current_user_admin():
            # update user status to 1
            counselor = Counselor.get_by_key_name(str(users.get_current_user().user_id()))
            counselor.status = 1
            counselor.put()
            
            # admin page
            self.redirect('/support')
            return      
            
class Login(AbstractHandler):
    def get(self):
        self.redirect(users.create_login_url('/'))
        
class Logout(AbstractHandler):
    def get(self):
        # update user status to 0
        counselor = Counselor.get_by_key_name(str(users.get_current_user().user_id()))
        counselor.status = 0
        counselor.put()
        
        self.redirect(users.create_logout_url('/'))  