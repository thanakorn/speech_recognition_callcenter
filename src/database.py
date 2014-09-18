__author__ = 'thanakorn'

from pymongo import MongoClient
from bson.objectid import ObjectId
from models.customer import Customer
from models.prepaid import Prepaid
from models.postpaid import Postpaid
from models.account import Account
from models.bill import Bill
from models.setup import Setup
from models.howtopay import HowToPay
from models.howtotopup import HowToTopup


class Database(object):

    client = MongoClient('localhost', 27017)
    db = client['callcenter']

    @classmethod
    def find_by_id(cls, collection, id):
        if collection == 'customers':
            return Customer.fromjson(cls.db[collection].find_one({'_id': ObjectId(id)}))
        if collection == 'prepaids':
            return Prepaid.fromjson(cls.db[collection].find_one({'_id': ObjectId(id)}))
        if collection == 'postpaids':
            return Postpaid.fromjson(cls.db[collection].find_one({'_id': ObjectId(id)}))
        if collection == 'accounts':
            return Account.fromjson(cls.db[collection].find_one({'_id': ObjectId(id)}))
        if collection == 'bills':
            return Bill.fromjson(cls.db[collection].find_one({'_id': ObjectId(id)}))

    @classmethod
    def find_one(cls, collection, field, value):
        if collection == 'customers':
            return Customer.fromjson(cls.db[collection].find_one({field: value}))
        if collection == 'prepaids':
            return Prepaid.fromjson(cls.db[collection].find_one({field: value}))
        if collection == 'postpaids':
            return Postpaid.fromjson(cls.db[collection].find_one({field: value}))
        if collection == 'setups':
            return Setup.fromjson(cls.db[collection].find_one({field: value}))
        if collection == 'how_to_pays':
            return HowToPay.fromjson(cls.db[collection].find_one({field: value}))
        if collection == 'how_to_topups':
            return HowToTopup.fromjson(cls.db[collection].find_one({field: value}))
        if collection == 'accounts':
            account = cls.db[collection].find_one({field: value})
            if account is not None:
                return Account.fromjson(cls.find_by_id('customers', account['customer']), cls.find_by_id('prepaids', account['package']), account)
            else:
                return None
        if collection == 'bills':
            bill = cls.db[collection].find({field: value}).sort('payment_date', -1)[0]
            if bill is not None:
                return Bill.fromjson(bill, cls.find_by_id('customers', bill['customer']), cls.find_by_id('postpaids', bill['package']))
            else:
                return None

    @classmethod
    def find_list(cls, collection, field, value):
        list = []
        results = cls.db[collection].find({field: value})
        for result in results:
            if collection == 'customers':
                list.append(Customer.fromjson(result))
            elif collection == 'prepaids':
                list.append(Prepaid.fromjson(result))
            elif collection == 'postpaids':
                list.append(Postpaid.fromjson(result))
            elif collection == 'accounts':
                list.append(Account.fromjson(result))
            elif collection == 'bills':
                list.append(Bill.fromjson(result))
        return list

    @classmethod
    def find_user_account(cls, id):
        account = cls.find_one('accounts', 'customer', ObjectId(id))
        if account is not None:
            return account

        bill = cls.find_one('bills', 'customer', ObjectId(id))
        if bill is not None:
            return bill

    @classmethod
    def update(cls, collection, condition_field, condition_value, update_field, update_value):
        cls.db[collection].update({condition_field: ObjectId(condition_value)}, {'$set': {update_field: ObjectId(update_value)}})

    @classmethod
    def insert(cls, collection, json):
        cls.db[collection].insert(json)


if __name__ == '__main__':
    pass
