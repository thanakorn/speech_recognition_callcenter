__author__ = 'thanakorn'

class HowToTopup(object):

    def __init__(self, id, method, step):
        self.id = id
        self.method = method
        self.step = step

    @classmethod
    def fromjson(cls, json):
        if json is None:
            return None
        return cls(json['_id'], json['method'], json['step'])