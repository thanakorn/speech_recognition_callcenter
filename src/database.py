from src.models.postpaid import Postpaid

__author__ = 'thanakorn'

from pymongo import MongoClient
from bson.objectid import ObjectId
from models.customer import Customer
from models.prepaid import Prepaid
from models.postpaid import Postpaid
from models.account import Account
from models.bill import Bill


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
        if collection == 'accounts':
            return Account.fromjson(cls.find_one('customers', field, value), cls.find_one('prepaids', field, value),cls.db[collection].find_one({field: value}))
        if collection == 'bills':
            return Bill.fromjson(cls.find_one('customers', field, value), cls.find_one('prepaids', field, value),cls.db[collection].find_one({field: value}))

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

if __name__ == '__main__':
    pass
