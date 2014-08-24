__author__ = 'thanakorn'


class Follwer(object):

    def __init__(self):
        pass

    def follow(self, publisher):
        publisher.add_follower(self)

    def receive(self, msg):
        pass
