__author__ = 'thanakorn'


import os


class Keyword:

    def __init__(self):
        self.keywords = {}
        filename = os.path.dirname(os.getcwd()) + '/conf/keyword/keywords.txt'
        file = open(filename, 'r')
        lines = file.readlines()
        for line in lines:
            key = line.strip().split('=')[0].strip()
            words = line.split('=')[1].strip().split(',')
            self.keywords.update({key: words})
        file.close()

    def contains_keyword(self, key, sentence):
        for keyword in self.keywords[key]:
            if keyword in sentence:
                return True
        return False
