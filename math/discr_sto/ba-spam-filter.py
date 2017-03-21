class SpamFilter(object):
    def __init__(self, arg):
        pass

    def is_spam(self, email):
        words = [word for word in re.split('[.!?,:;]|\s', fl.read()) if len(word)>1 or word in ['I', 'i']]




def is_spam(fl_name, threshold):

    with open(fl_name, 'r') as fl:
        import re

        words = [word for word in re.split('[.!?,:;]|\s', fl.read()) if len(word)>1 or word in ['I', 'i']]

        spam_prob = 0
        for word in words:
            pass

def train():
    for value in variable:
        pass

if __name__ == "__main__":
    import os
    filter = SpamFilter()


    with open(fl_name, 'r') as fl:
