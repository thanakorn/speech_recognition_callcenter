__author__ = 'thanakorn'

from src.follower import Follwer
from src.speech_recognizer import SpeechRecognizer


class Callcenter(Follwer):

    def __init__(self):
        Follwer.__init__(self)
        self.recognizer = SpeechRecognizer()
        self.follow(self.recognizer)
        self.recognizer.start()

    def receive(self, msg):
        print('Callcenter receive msg : ' + msg)
