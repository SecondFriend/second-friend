from handlers import AbstractHandler

from models import Configo, Counselor
from google.appengine.api import users, images, urlfetch
from google.appengine.ext import db

import logging
import settings

class Update(AbstractHandler):
    # update the counselor profile
    def post(self):
        counselor = Counselor.get_or_insert(str(users.get_current_user().user_id()))

        if self.request.get('avatar'):
            counselor.avatar = db.Blob(images.resize(self.request.get('avatar'), 90, 90))
            
        counselor.name =  self.request.get('name')
        counselor.expertises = self.request.POST.getall('expertises')
        counselor.put()
        
        self.redirect('/counselor/edit?saved=1')
        
class Edit(AbstractHandler):
    # render counselor edit screen
    def get(self):
        counselor = Counselor.get_or_insert(str(users.get_current_user().user_id()))
        
        # list of expertises
        _expertises = ['Cyberbully', 'Child Rights', 'Sexual Abuse', 'Teen Relationship', 'Drugs', 'School Stress', 'Parenting']
        
        template_vars = {
            'saved': self.request.get('saved'),
            'id': str(users.get_current_user().user_id()),
            'counselor': counselor,
            '_expertises': _expertises
        }

        self._output_template('counselor-edit.html', **template_vars)
        
class Avatar(AbstractHandler):
    # return counselor image
    def get(self):
        counselor = Counselor.get_by_key_name(str(self.request.get('key')))
        
        if counselor.avatar:
            self.response.headers['Content-Type'] = "image/jpg"
            self.response.out.write(counselor.avatar)
        else:
            self.response.headers['Content-Type'] = "image/jpg"
            self.response.out.write(urlfetch.Fetch('https://second-friend.appspot.com/static/img/avatar.jpg').content)
