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
    
    # support
    ('/support', 'handlers.support.Support'),
    
    # counselor
    ('/counselor/update', 'handlers.counselor.Update'),
    ('/counselor/edit', 'handlers.counselor.Edit'),
    ('/counselor/avatar', 'handlers.counselor.Avatar'),
    
    # route
    ('/route/create', 'handlers.route.Queue'),
    ('/route/queue', 'handlers.route.Queue'),
    
    ('/route/remove', 'handlers.route.Remove'),
    ('/route/assign', 'handlers.route.Assign'),
    ('/route/transfer', 'handlers.route.Transfer'),
    
]

app = webapp2.WSGIApplication(
    routes = routes,
    debug = settings.DEBUG,
    config = settings.config,
)
