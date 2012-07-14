# imports
import webapp2
import settings

import sys
sys.path.append('libs')

# routes
routes = [    
    # welcome page
    ('/', 'handlers.index.Index'),
    ('/login', 'handlers.index.Login'),
    ('/logout', 'handlers.index.Logout'),
    
    # counselor - profile, avatar, etc
    ('/counselor/update', 'handlers.counselor.Update'),
    ('/counselor/edit', 'handlers.counselor.Edit'),
    ('/counselor/avatar', 'handlers.counselor.Avatar'),

    # support - main support chat page
    ('/support', 'handlers.support.Index'),
    
    # route - route incoming chat requests to available counselors
    ('/route/create', 'handlers.route.Queue'),
    ('/route/queue', 'handlers.route.Queue'),
    
    ('/route/remove', 'handlers.route.Remove'),
    ('/route/assign', 'handlers.route.Assign'),
    ('/route/transfer', 'handlers.route.Transfer'),
    
]

# run the app
app = webapp2.WSGIApplication(
    routes = routes,
    debug = settings.DEBUG,
    config = settings.config,
)
