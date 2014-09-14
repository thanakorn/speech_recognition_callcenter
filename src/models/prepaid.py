__author__ = 'thanakorn'


class Prepaid(object):

    def __init__(self, id, name, type, internal_calling_rate, external_calling_rate, internet_data, internet_rate, sms_rate, free_wifi, wifi_rate, initial_balance, initial_date, registration_fee, payment):
        self.id = id
        self.name = name
        self.type = type
        self.internal_calling_rate = internal_calling_rate
        self.external_calling_rate = external_calling_rate
        self.internet_data = internet_data
        self.internet_rate = internet_rate
        self.sms_rate = sms_rate
        self.free_wifi = free_wifi
        self.wifi_rate = wifi_rate
        self.initial_balance = initial_balance
        self.initial_date = initial_date
        self.registration_fee = registration_fee
        self.payment = payment

    @classmethod
    def fromjson(cls, json):
        if json is None:
            return None
        return cls(json['_id'], json['name'], json['type'], json['internal_calling_rate'], json['external_calling_rate'], json['internet_data'], json['internet_rate'], json['sms_rate'], json['free_wifi'], json['wifi_rate'], json['initial_balance'], json['initial_date'], json['registration_fee'], json['payment'])

    def is_internet_unlimited(self):
        return self.internet_data == -1

    def is_unlimited_wifi(self):
        return self.free_wifi == -1

    def is_internet_avail(self):
        return self.internet_rate == -1 or self.internet_rate > 0

    def description(self):
        return '%s package registration fee is %d baht. calling rate is %d baht per minute. sms rate is %d baht per message. initial balance is %d baht and initial date is %d days' % (self.name, self.registration_fee, self.internal_calling_rate, self.sms_rate, self.initial_balance, self.initial_date)
