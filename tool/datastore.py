#coding=utf-8
import logging

from google.appengine.ext import ndb
from datetime import datetime


def get_from_urlsafe(urlsafe, keys_only=False):
    key = ndb.Key(urlsafe=urlsafe)
    if keys_only:
        return key
    return key.get()


class User(ndb.Model):
    # user name
    name = ndb.StringProperty(required=True)
    # user faces
    img_key = ndb.KeyProperty()
    # user chatclass
    chatclass = ndb.IntegerProperty(required=True)
    # time
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    # normal user
    account = ndb.StringProperty()
    passward = ndb.StringProperty()
    # FB user
    fbuser = ndb.BooleanProperty(required=True)
    fid = ndb.StringProperty()
    profile_url = ndb.StringProperty()
    access_token = ndb.StringProperty()

    @staticmethod
    def parent_key():
        return ndb.Key('/','user')

    @classmethod
    def by_fid(cls,fid):
        q = cls.query(ancestor=cls.parent_key())
        q = q.filter(cls.fid==fid)
        return q.get()

    @classmethod
    def by_id(cls,uid):
        return cls.get_by_id(uid,parent=cls.parent_key())

    @classmethod
    def by_account(cls, account, *a, **kw):
        q = cls.query(ancestor=cls.parent_key(),)
        q = q.filter(cls.account==account)
        return q.get(*a,**kw)


class Image(ndb.Model):
    img = ndb.BlobProperty(indexed=False)
    img_type = ndb.StringProperty(indexed=False)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def parent_key(compression='origin'):
        return ndb.Key('/',compression)

    @classmethod
    def by_id(cls, imgid, compression='origin'):
        return cls.get_by_id(imgid,parent=cls.parent_key(compression))


# The post of Question, Discus, technology, Amazing.
class Post(ndb.Model):
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty()
    post_tpye = ndb.StringProperty(required=True)
    # author
    author = ndb.KeyProperty(required=True)
    # time
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    # evaluation, type is a list of Datastore Key to users
    good = ndb.KeyProperty(repeated=True)
    bad = ndb.KeyProperty(repeated=True)

    @staticmethod
    def parent_key(path='/'):
        return ndb.Key(path,'post')


class Message(ndb.Model):
    content = ndb.StringProperty(required=True)
    author = ndb.KeyProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def room_key(room):
        return ndb.Key(room,'message')

    @classmethod
    def by_ancestor(cls, ancestor, time=datetime.now()):
        q = cls.query(ancestor=ancestor)
        q = q.order(-cls.created)
        return q.fetch(limit=10)
