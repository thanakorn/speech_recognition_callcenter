__author__ = 'thanakorn'

from subprocess import call


class Speaker:

    def __init__(self):
        pass

    @staticmethod
    def speak(msg):
        for sentence in msg.split('. '):
            call(['sapitest', sentence + '.', '-v', 'Mary', '-s', '0.9'])
