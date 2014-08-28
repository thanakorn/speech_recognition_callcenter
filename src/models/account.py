__author__ = 'thanakorn'


class Account(object):

    def __init__(self, id, customer, package, balance, expiration_date):
        self.id = id
        self.customer = customer
        self.package = package
        self.balance = balance
        self.expiration_date = expiration_date

    @classmethod
    def fromjson(cls, customer, package, json):
        cls(json['_id'], customer, package, json['balance'], json['expiration_date'])
