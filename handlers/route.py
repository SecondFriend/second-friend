from handlers import AbstractHandler

from models import Configo, Counselor
from google.appengine.api import users, taskqueue

from pubnub import Pubnub

import logging
import settings

### pubnub instance
pubnub = Pubnub(
    'pub-91077960-1dd7-4875-83c4-c8fd5c634bee', 
    'sub-786b929e-bab1-11e1-b880-a3fb466a40d5',
    'sec-YWNjYmIxZmYtZTVkZS00ZGNlLTk0NWUtYWRhZTk5OGUzN2Y1',
    False
)

class Queue(AbstractHandler):
    def get(self):
        uuid = self.request.get('channel') #self.request.get('uuid')
        channel = self.request.get('channel')
        
        # check if the kid channel already has an assigned counselor
        counselors = Counselor.all()
        counselors.filter('status >', 0)
        counselors.filter('channels IN', [channel])
        counselors = counselors.fetch(1)
                
        if len(counselors):
            logging.info('already assigned')
            
            counselor = counselors[0]
            
            # publish the counselor profile
            info = pubnub.publish({
                #'channel' : 'kid-'+ kid,
                'channel': channel,
                'message' : {
                    'type': 'system',
                    'timestamp': '',
                    'payload': {
                        'action': 'counselor',
                        'avatar': 'https://super-support.appspot.com/counselor/avatar?key='+ counselor.key().name(),
                        'name': counselor.name,
                        'id': counselor.key().name(),
                    }
                }
            })
            
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.set_status(200)
            self.response.out.write('already assigned')
            return
            
        # add to task queue
        taskqueue.add(queue_name = 'QueueRoute', url = '/route/assign', params = { 
            'uuid': uuid, 
            'channel': channel,
        }, method = 'GET', )
        
        # publish a message
        info = pubnub.publish({
            #'channel' : 'kid-'+ channel,
            'channel': channel,
            'message' : {
                'type': 'status',
                'sender': 'SecondFriend',
                'timestamp': '',
                'payload': 'Hello! You will be assigned to a counselor shortly.',
            }
        })
        
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.set_status(202)
        self.response.out.write('queued')
        
class Assign(AbstractHandler):
    def get(self):
        uuid = self.request.get('channel') #self.request.get('uuid')
        channel = self.request.get('channel')
        
        # check available counselors
        counselors = Counselor.all()
        counselors.filter('status >', 0)
        counselors = counselors.fetch(3)
        
        counselor = counselors[0]
        
        # assign to counselor with the least channel
        for c in counselors:
            if(len(c.channels) < len(counselor.channels)):
                counselor = c
                        
        # no counselor available
        if not len(counselors):
            logging.info('no counselor available')
            
            self.response.headers['Access-Control-Allow-Origin'] = '*'
            self.response.set_status(500)
            self.response.out.write('no counselor available')
            return

        # update the counselor model - channels
        if (channel not in counselor.channels):
            counselor.channels.append(channel)
            counselor.put()
                    
        # assign and inform the counselor
        # publish the command for counselor screen
        info = pubnub.publish({
            'channel' : 'counselor-'+ counselor.key().name(),
            'message' : {
                'action': 'create',
                'uuid': uuid,
                'channel' : channel
            }
        })

        # publish the counselor profile
        info = pubnub.publish({
            #'channel' : 'kid-'+ kid,
            'channel': channel,
            'message' : {
                'type': 'system',
                'timestamp': '',
                'payload': {
                    'action': 'counselor',
                    'avatar': 'https://super-support.appspot.com/counselor/avatar?key='+ counselor.key().name(),
                    'name': counselor.name,
                    'id': counselor.key().name(),
                }
            }
        })
        
        # publish a message
        info = pubnub.publish({
            #'channel' : 'kid-'+ channel,
            'channel': channel,
            'message' : {
                'type': 'status',
                'sender': 'SecondFriend',
                'payload': 'You have been assigned a counselor.',
            }
        })
        
        logging.info(counselor.name)
        logging.info(counselor.key().name())

        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.set_status(200)
        self.response.out.write('assigned')
        
        
# transfer is basically (assign -> remove) or (queue -> assign -> remove)        
class Transfer(AbstractHandler):
    def get(self):
        pass

class Remove(AbstractHandler):
    def get(self):
        uuid = self.request.get('channel') #self.request.get('uuid')
        channel = self.request.get('channel')
        purge = self.request.get('purge') # Counselor.key().name()
        
        counselor = False
        if purge:
            counselor = Counselor.get_by_key_name(purge)
        else:
            counselors = Counselor.all()
            #counselors.filter('status >', 0)
            #counselors.filter('channels IN', [channel])
            counselors = counselors.fetch(10)
        
        
            for c in counselors:
                if channel in c.channels:
                    counselor = c
                    break

        if counselor:
            if not purge and channel in counselor.channels:
                counselor.channels.remove(channel)
            
            if purge:
                counselor.channels = []
                
            counselor.put()
        
            # publish the command
            info = pubnub.publish({
                'channel' : 'counselor-'+ counselor.key().name(),
                'message' : {
                    'action': 'purge' if purge else 'remove',
                    'uuid': uuid,
                    'channel' : channel
                }
            })
        
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.set_status(200)
        self.response.out.write('removed')