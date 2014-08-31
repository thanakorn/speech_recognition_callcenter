__author__ = 'thanakorn'

from bson.objectid import ObjectId
import datetime


class Bill(object):

    def __init__(self, customer, package, calling_time, sms, internet, wifi, payment_date, paid, id=None):
        if id is None:
            self.id = ObjectId()
        else:
            self.id = id
        self.customer = customer
        self.package = package
        self.calling_time = calling_time
        self.sms = sms
        self.internet = internet
        self.wifi = wifi
        self.payment_date = payment_date
        self.paid = True if paid == 1 else False

    @classmethod
    def fromjson(cls, customer, package, json):
        if json is None:
            return None
        return cls(customer, package, json['calling_time'], json['sms'], json['internet'], json['wifi'], json['payment_date'], json['paid'], json['_id'])

    def tojson(self):
        json = {
            '_id': ObjectId(),
            'customer': ObjectId(self.customer.id),
            'package': ObjectId(self.package.id),
            'calling_time': self.calling_time,
            'sms': self.sms,
            'internet': self.internet,
            'wifi': self.wifi,
            'payment_date': self.payment_date,
            'paid': 1 if self.paid else 0
        }
        return json

    def total(self):
        total = self.package.fee
        if self.calling_time > self.package.calling_time:
            total += (self.calling_time - self.package.calling_time) * self.package.extra_call_rate
        if self.sms > 0:
            total += self.sms * self.package.sms_rate
        return total

    def is_overdue(self):
        return not self.paid and (datetime.datetime.now() > self.payment_date)