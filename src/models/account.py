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
        if json is None:
            return None
        return cls(json['_id'], customer, package, json['balance'], json['expiration_date'])

    def report(self):
        return str('Your current balance is %d baht expire on %s %s %s.' % (self.balance, self.expiration_date.strftime('%d'), self.expiration_date.strftime('%B'), self.expiration_date.strftime('%Y')))