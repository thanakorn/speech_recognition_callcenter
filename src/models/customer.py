__author__ = 'thanakorn'


class Customer(object):

    def __init__(self, firstname, lastname, age, gender, phone_number):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.gender = gender
        self.phone_number = phone_number
        self.fullname = self.firstname + ' ' + self.lastname

    @classmethod
    def fromjson(cls, json):
        return cls(json['firstname'], json['lastname'], json['age'], json['gender'], json['phone_number'])
