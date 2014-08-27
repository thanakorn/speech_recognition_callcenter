__author__ = 'thanakorn'

from pymongo import MongoClient
from bson.objectid import ObjectId
from models.customer import Customer

class Database(object):

    def __init__(self):
        """ Initial MongoDB client """
        client = MongoClient('localhost', 27017)
        db = client['callcenter']
        self.customers = db['customers']
        self.postpaid = db['postpaid']
        self.prepaid = db['prepaid']
        self.enhanced_packages = db['enhanced_packages']
        self.bills = db['bills']
        self.accounts = db['accounts']

    def find_customer(self, field, value):
        return Customer.fromjson(self.customers.find_one({field: value}))
