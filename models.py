from google.appengine.ext import db, blobstore
from google.appengine.api import memcache

import logging

class Counselor(db.Model):
    userid = db.StringProperty()
    name = db.StringProperty()
    
    avatar = db.BlobProperty(default=None)
    
    expertises = db.StringListProperty()
    channels = db.StringListProperty(default=[])
    organization = db.StringProperty()
    
    # 0 - not available, 1 - available
    status = db.IntegerProperty(default=0)
    
    created = db.DateTimeProperty(auto_now_add=True)
        
class Configo(db.Model):
    """data model for config key-value pairs"""
    val = db.StringProperty()

    @classmethod
    def get(cls, key, default = None):
        # get from memcache
        val = memcache.get(key) 
        
        # if not, try to get from datastore
        if not memcache.get(key) and cls.get_by_key_name(key):
            val = cls.get_by_key_name(key).val

        # if val, then return it ... else return default
        return val if val else default 

    @classmethod
    def set(cls, key, val):
        # save in memcache
        if not memcache.set(key, val):
            # if memcache fails to save, clear the cached value and quit
            memcache.delete(key)
            return False

        # save in db
        if cls(key_name=key, val=val).put():
            return True

        return False