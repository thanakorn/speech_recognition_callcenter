__author__ = 'thanakorn'


class Publisher(object):

    def __init__(self):
        self.follwers = []

    def add_follower(self, follower):
        self.follwers.append(follower)

    def pulish(self, msg):
        for follower in self.follwers:
            follower.receive(msg)
