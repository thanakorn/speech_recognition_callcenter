__author__ = 'thanakorn'


class Postpaid(object):

    def __init__(self, id, name, type, calling_time, extra_call_rate, internet_data, max_internet_speed, max_speed_data, overlimit_internet_speed, sms_rate, free_wifi, fee, payment):
        self.id = id
        self.name = name
        self.type = type
        self.calling_time = calling_time
        self.extra_call_rate = extra_call_rate
        self.internet_data = internet_data
        self.max_internet_speed = max_internet_speed
        self.max_speed_data = max_speed_data
        self.overlimit_internet_speed = overlimit_internet_speed
        self.sms_rate = sms_rate
        self.free_wifi = free_wifi
        self.fee = fee
        self.payment = payment

    @classmethod
    def fromjson(cls, json):
        if json is None:
            return None
        return cls(json['_id'], json['name'], json['type'], json['calling_time'], json['extra_calling_rate'], json['internet_data'], json['max_internet_speed'], json['max_speed_data'], json['overlimit_internet_speed'], json['sms_rate'], json['free_wifi'], json['fee'], json['payment'])

    def is_internet_unlimited(self):
        return self.internet_data == -1

    def is_unlimited_wifi(self):
        return self.free_wifi == -1

    def is_internet_avail(self):
        return self.internet_data == -1 or self.internet_data > 0

    def description(self):
        return '%s package monthly fee is %d bahts. maximum calling time is %d minutes. you will be able to use internet at maximum speed for %.2f gigabytes. after reach the limit, internet speed will limit to %d kilobytes and SMS rate is %.2f bahts per message' % (self.name, self.fee, self.calling_time, self.max_speed_data, self.overlimit_internet_speed, self.sms_rate)
