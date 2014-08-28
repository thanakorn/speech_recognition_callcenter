__author__ = 'thanakorn'


import os


class KeywordProcessing(object):

    keywords = {}
    filename = os.path.dirname(os.getcwd()) + '/conf/keyword/keywords.txt'
    file = open(filename, 'r')
    lines = file.readlines()
    for line in lines:
        key = line.strip().split('=')[0].strip()
        words = line.split('=')[1].strip().split(',')
        keywords.update({key: words})
    file.close()

    @classmethod
    def contains_keyword(cls, key, sentence):
        for keyword in cls.keywords[key]:
            if keyword in sentence:
                return True
        return False
