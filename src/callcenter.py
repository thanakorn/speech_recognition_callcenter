__author__ = 'thanakorn'

from src.follower import Follwer
from src.speech_recognizer import SpeechRecognizer
from src.state import State
from keyword_processing import KeywordProcessing
from speaker import Speaker
from database import Database
from models.bill import Bill
import datetime


class Callcenter(Follwer):

    def __init__(self):
        Follwer.__init__(self)
        self.state = State.NORMAL
        self.recognizer = SpeechRecognizer()
        self.follow(self.recognizer)
        self.answer = str()
        self.recommend_packages = []
        self.interesting_package = None

        Speaker.speak('Please tell your phone number.')
        # number = raw_input('Phone number : ')
        number = '0836990198'  # postpaid dummy
        # number = '0879987123'  # prepaid dummy
        self.current_user = Database.find_one('customers', 'phone_number', number)
        self.user_account = Database.find_user_account(self.current_user.id)
        # If phone no is exist, Greeting
        if self.current_user is not None:
            Speaker.speak('Good morning mister %s. How can i help you.' % self.current_user.fullname())
            self.recognizer.start()
        # Otherwise, Goodbye
        else:
            Speaker.speak('Sorry. Your number is not in our system.')

    def receive(self, msg):
        self.recognizer.stop()      # Pause Speech recognizer

        print('Callcenter receive msg : ' + msg)

        if self.state == State.NORMAL:
            if KeywordProcessing.contains_keyword('package', msg):
                # Current package
                if KeywordProcessing.contains_keyword('current', msg):
                    self.answer = str('Your current package is %s' % self.user_account.package.description())
                    # Change state
                    self.state = State.REPEAT
                # Recommend package
                elif KeywordProcessing.contains_keyword('package_category', msg):
                    package_category = [c for c in KeywordProcessing.keywords['package_category'] if c in msg][0]
                    # Find interesting packages
                    if self.user_account.package.payment == 'prepaid':
                        self.recommend_packages = Database.find_list('prepaids', 'type', package_category)
                    else:
                        self.recommend_packages = Database.find_list('postpaids', 'type', package_category)

                    # Generate answer
                    self.answer = str('We recommend %d packages for you. ' % len(self.recommend_packages))
                    for package in self.recommend_packages:
                        self.answer += package.name + '. '
                    self.answer += str('Which one you want to have a detail. Or you want to listen again.')
                    # Change state
                    self.state = State.SELECT_PACKAGE

        elif self.state == State.REPEAT:
            # Repeat
            if KeywordProcessing.contains_keyword('confirm', msg):
                pass
            # Back to normal
            elif KeywordProcessing.contains_keyword('cancel', msg):
                self.answer = 'How can i help you?'
                self.state = State.NORMAL

        elif self.state == State.SELECT_PACKAGE:
            # Repeat
            if KeywordProcessing.contains_keyword('confirm', msg):
                pass
            # Explain user's interesting package detail
            elif KeywordProcessing.contains_keyword('ordinal', msg):
                index = KeywordProcessing.get_index(msg) - 1
                self.interesting_package = self.recommend_packages[index]
                self.answer = str(self.interesting_package.description())
                self.answer += str(' Do you want to use this package.')
                self.state = State.CHANGE_PACKAGE

        elif self.state == State.CHANGE_PACKAGE:
            if KeywordProcessing.contains_keyword('confirm', msg):
                if self.user_account.package.payment == 'prepaid':
                    # Change package of account
                    Database.update('accounts', 'customer', self.current_user.id, 'package', self.interesting_package.id)
                elif self.user_account.package.payment == 'postpaid':
                    # Create new bill
                    new_bill = Bill(self.current_user, self.interesting_package, 0, 0, 0, 0, datetime.datetime.now(), 0)
                    Database.insert('bills', new_bill.tojson())
                self.answer = 'package change is complete.'
                # Get new user account
                self.user_account = Database.find_user_account(self.current_user.id)
                self.state = State.NORMAL
            elif KeywordProcessing.contains_keyword('cancel', msg):
                self.state = State.NORMAL

        if self.answer is not None:
            Speaker.speak(self.answer)

        if self.state == State.REPEAT:
            Speaker.speak('Do you want to listen again.')

        self.recognizer.resume()    # Resume Speech recognizer

if __name__ == '__main__':
    callcenter = Callcenter()
