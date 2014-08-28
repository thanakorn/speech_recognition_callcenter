__author__ = 'thanakorn'


class Bill(object):

    def __init__(self, id, calling_time, sms, internet, wifi, payment_date, paid):
        self.id = id
        self.calling_time = calling_time
        self.sms = sms
        self.internet = internet
        self.wifi = wifi
        self.payment_date = payment_date
        self.paid = True if paid == 1 else False
        pass

    @classmethod
    def fromjson(cls, customer, package,json):
        cls(json['_id'], customer, package, json['calling_time'], json['sms'], json['internet'], json['wifi'], json['payment_date'], json['paid'])

