__author__ = 'thanakorn'

from subprocess import call


class Speaker:

    def __init__(self):
        pass

    @staticmethod
    def speak(msg):
        call(['sapitest', msg, '-v', 'Mary', '-s', '0.8'])
