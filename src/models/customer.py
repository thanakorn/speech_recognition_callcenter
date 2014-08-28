__author__ = 'thanakorn'


class Customer(object):

    def __init__(self, id, firstname, lastname, age, gender, phone_number):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.phone_number = phone_number

    def fullname(self):
        return self.firstname + ' ' + self.lastname

    @classmethod
    def fromjson(cls, json):
        if json is None:
            return None
        return cls(json['_id'], json['firstname'], json['lastname'], json['age'], json['gender'], json['phone_number'])
