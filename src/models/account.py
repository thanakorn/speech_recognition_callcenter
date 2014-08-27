__author__ = 'thanakorn'

from src.database import Database


class Account(object):

    db = Database()

    def __init__(self, id, customer, package, balance, expiration_date):
        self.id = id
        self.customer = customer
        self.package = package
        self.balance = balance
        self.expiration_date = expiration_date

    @classmethod
    def fromjson(cls, json):
        customer = cls.db.find_by_id('customers', json['customer'])
        package = cls.db.find_by_id('prepaid', json['package'])
        cls(json['_id'], customer, package, json['balance'], json['expiration_date'])
