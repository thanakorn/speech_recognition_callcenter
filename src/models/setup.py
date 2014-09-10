__author__ = 'thanakorn'


class Setup(object):

    def __init__(self, id, os, setup):
        self.id = id
        self.os = os
        self.setup = setup

    @classmethod
    def fromjson(cls, json):
        if json is None:
            return None
        return cls(json['_id'], json['os'], json['setup'])
