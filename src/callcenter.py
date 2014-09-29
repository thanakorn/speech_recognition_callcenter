__author__ = 'thanakorn'

from follower import Follwer
from speech_recognizer import SpeechRecognizer
from state import State
from keyword_processing import KeywordProcessing
from speaker import Speaker
from database import Database
from models.bill import Bill
from bson.objectid import ObjectId
import datetime
from subprocess import call


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
        number = raw_input('Phone number : ')
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

        if KeywordProcessing.contains_keyword('exit', msg):
            self.answer = str('Do you want to exit.')
            self.state = State.EXIT_CONFIRM
        elif KeywordProcessing.contains_keyword('reset', msg):
            self.answer = str('How can i help you.')
            self.state = State.NORMAL
        elif KeywordProcessing.contains_keyword('operator', msg):
            self.answer = str('Do you want to talk to operator.')
            self.state = State.TALK_TO_OPERATOR
        elif self.state == State.NORMAL:
            # Package category
            if KeywordProcessing.contains_keyword('package', msg):
                # Recommend package
                if KeywordProcessing.contains_keyword('package_category', msg):
                    package_category = [c for c in KeywordProcessing.keywords['package_category'] if c in msg][0]
                    # Find interesting packages
                    if self.user_account.package.payment == 'prepaid':
                        self.recommend_packages = Database.find_list('prepaids', 'type', package_category)
                    else:
                        self.recommend_packages = Database.find_list('postpaids', 'type', package_category)
                    # Generate answer
                    self.answer = str('We recommend %d packages for you. ' % len(self.recommend_packages))
                    index = 1
                    for package in self.recommend_packages:
                        self.answer += str('package number %d %s . ' % (index, package.name))
                        index += 1
                    self.answer += str('Which one you want to have a detail. Or you want to listen again.')
                    self.state = State.SELECT_PACKAGE   # Change state
                # Current package
                else:
                    self.answer = str('Your current package is %s' % self.user_account.package.description())
                    self.state = State.REPEAT   # Change state

            # How to
            elif KeywordProcessing.contains_keyword('how_to', msg):
                if KeywordProcessing.contains_keyword('topup', msg):
                    self.answer = str('Please select your topup method. Online or phone.')
                    self.state = State.SELECT_TOPUP_METHOD
                elif KeywordProcessing.contains_keyword('pay', msg):
                    self.answer = str('Please select your payment method. Online or phone.')
                    self.state = State.SELECT_PAYMENT_METHOD
                elif KeywordProcessing.contains_keyword('setup', msg):
                    self.answer = str('What is your operating system.')
                    self.state = State.SELECT_PHONE_OS

            # Bill category
            elif KeywordProcessing.contains_keyword('balance', msg) or KeywordProcessing.contains_keyword('expire', msg):
                if self.user_account.package.payment == 'postpaid':
                    self.answer = str('Sorry, I don\'t understand your question')
                elif KeywordProcessing.contains_keyword('balance', msg):
                    self.answer = self.user_account.report()
                    self.state = State.REPEAT
                elif KeywordProcessing.contains_keyword('expire', msg):
                    self.answer = str('Your account will expire on %s %s %s.' % (self.user_account.expiration_date.strftime('%d'), self.user_account.expiration_date.strftime('%B'), self.user_account.expiration_date.strftime('%Y')))
                    self.state = State.REPEAT

            elif KeywordProcessing.contains_keyword('bill', msg):
                if self.user_account.package.payment == 'postpaid':
                    if KeywordProcessing.contains_keyword('unpaid', msg):
                        all_bills = Database.find_list('bills', 'customer', ObjectId(self.current_user.id))
                        unpaid_bills = [bill for bill in all_bills if not bill.paid]
                        if(len(unpaid_bills) > 0):
                            self.answer = str('You have %d bills unpaid.' % len(unpaid_bills))
                        else:
                            self.answer = str('You don\' have any unpaid bill.')
                    elif KeywordProcessing.contains_keyword('how_to', msg) and KeywordProcessing.contains_keyword('pay', msg):
                        self.answer = str('Please select your payment method. Online or phone.')
                        self.state = State.SELECT_PAYMENT_METHOD
                    elif KeywordProcessing.contains_keyword('when', msg):
                        self.answer = str('Your bill is due on %d %s.' % (self.user_account.payment_date.strftime('%d'), self.user_account.payment_date.strftime('%B')))
                    else:
                        self.answer = self.user_account.report()
                        self.state = State.REPEAT
                else:
                    self.answer = str('Sorry, I don\'t understand your question')

            # Troubleshooting
            elif KeywordProcessing.contains_keyword('cannot', msg):
                # Prepaid user
                if self.user_account.package.payment == 'prepaid':
                    if KeywordProcessing.contains_keyword('internet', msg):
                        if not self.user_account.package.is_internet_avail():
                            self.answer = str('Sorry, your current package is not support internet using.')
                        else:
                            self.answer = str('Sorry, i can\'t find any problem in your account. Do you want to talk to the operator.')
                            self.state = State.TALK_TO_OPERATOR
                    elif KeywordProcessing.contains_keyword('call', msg):
                        if self.user_account.balance <= self.user_account.package.internal_calling_rate:
                            self.answer = str('Sorry, your current balance is not enough.')
                        else:
                            self.answer = str('Sorry, i can\'t find any problem in your account. Do you want to talk to the operator.')
                            self.state = State.TALK_TO_OPERATOR

                #Postpaid user
                else:
                    if KeywordProcessing.contains_keyword('internet', msg):
                        if not self.user_account.package.is_internet_avail():
                            self.answer = str('Sorry, your current package is not support internet using.')
                        elif len([bill for bill in Database.find_list('bills', 'customer', self.current_user.id) if not bill.paid]) > 3:
                            self.answer = str('Sorry, your account was suspended because you haven\'t pay monthly fee.')
                        else:
                            self.answer = str('Sorry, i can\'t find any problem in your account. Do you want to talk to the operator.')
                            self.state = State.TALK_TO_OPERATOR
                    elif KeywordProcessing.contains_keyword('call', msg):
                        if self.user_account.package.payment == 'postpaid' and len([bill for bill in Database.find_list('bills', 'customer', self.current_user.id) if not bill.paid]) > 3:
                            self.answer = str('Sorry, your account was suspended because you haven\'t pay monthly fee.')
                        else:
                            self.answer = str('Sorry, i can\'t find any problem in your account. Do you want to talk to the operator.')
                            self.state = State.TALK_TO_OPERATOR

        elif self.state == State.REPEAT:
            # Repeat
            if KeywordProcessing.contains_keyword('confirm', msg):
                pass
            # Back to normal
            elif KeywordProcessing.contains_keyword('cancel', msg):
                self.answer = 'How can i help you.'
                self.state = State.NORMAL

        elif self.state == State.SELECT_PACKAGE:
            # Repeat
            if KeywordProcessing.contains_keyword('confirm', msg):
                pass
            elif KeywordProcessing.contains_keyword('cancel', msg):
                self.answer = 'How can i help you.'
                self.state = State.NORMAL
            # Explain user's interesting package detail
            elif KeywordProcessing.contains_keyword('ordinal', msg) and KeywordProcessing.get_index(msg) - 1 < len(self.recommend_packages):
                index = KeywordProcessing.get_index(msg) - 1
                self.interesting_package = self.recommend_packages[index]
                self.answer = str(self.interesting_package.description())
                self.answer += str(' Do you want to use this package.')
                self.state = State.CHANGE_PACKAGE
            else:
                self.answer = str('Sorry, i don\'t understand.')

        elif self.state == State.CHANGE_PACKAGE:
            if KeywordProcessing.contains_keyword('confirm', msg):
                if self.user_account.package.payment == 'prepaid':
                    # Change package of account
                    Database.update('accounts', 'customer', self.current_user.id, 'package', self.interesting_package.id)
                elif self.user_account.package.payment == 'postpaid':
                    # Create new bill
                    new_bill = Bill(self.current_user, self.interesting_package, 0, 0, 0, 0, datetime.datetime.now(), 0)
                    Database.insert('bills', new_bill.tojson())
                self.answer = 'package changing is complete.'
                # Get new user account
                self.user_account = Database.find_user_account(self.current_user.id)
                self.state = State.NORMAL
            elif KeywordProcessing.contains_keyword('cancel', msg):
                self.answer = 'How can i help you.'
                self.state = State.NORMAL
            else:
                self.answer = str('Sorry, i don\'t understand.')

        elif self.state == State.SELECT_PHONE_OS:
            if KeywordProcessing.contains_keyword('phone_os', msg):
                self.answer = Database.find_one('setups', 'os', msg).setup
                self.state = State.REPEAT
            else:
                self.answer = str('Sorry, we cannot find your operating system.')

        elif self.state == State.SELECT_PAYMENT_METHOD:
            if KeywordProcessing.contains_keyword('payment_method', msg):
                self.answer = Database.find_one('how_to_pays', 'method', msg).step
                self.state = State.REPEAT
            else:
                self.answer = str('Sorry, your payment method is not available.')

        elif self.state == State.SELECT_TOPUP_METHOD:
            if KeywordProcessing.contains_keyword('payment_method', msg):
                self.answer = Database.find_one('how_to_topups', 'method', msg).step
                self.state = State.REPEAT
            else:
                self.answer = str('Sorry, your payment method is not available.')

        elif self.state == State.TALK_TO_OPERATOR:
            if KeywordProcessing.contains_keyword('confirm', msg):
                self.answer = str('Transfer to operator. please wait for seconds.')
            elif KeywordProcessing.contains_keyword('cancel', msg):
                self.answer = str('How can i help you.')
                self.state = State.NORMAL

        elif self.state == State.EXIT_CONFIRM:
            if KeywordProcessing.contains_keyword('confirm', msg):
                self.answer = str('Thank you for using our service')
                self.state = State.EXIT
                self.recognizer.shutdown()
            elif KeywordProcessing.contains_keyword('cancel', msg):
                self.answer = str('How can i help you')
                self.state = State.NORMAL

        if self.answer is not None:
            Speaker.speak(self.answer)

        if self.state == State.REPEAT:
            Speaker.speak('Do you want to listen again.')

        self.recognizer.resume()    # Resume Speech recognizer

if __name__ == '__main__':
    call(['sh', ' ~/bin/sapi_server.sh'])  # Start SAPI service
    callcenter = Callcenter()