# I followed this naive Bayes classifier - http://www.cs.ubbcluj.ro/~gabis/DocDiplome/Bayesian/000539771r.pdf

class SpamFilter(object):
    from math import log

    def __init__(self):
        self.spam_prob_for_unknown_word = 0.5

        self.pS = None
        self.pJ = None
        self.log_pS_div_pJ = log(pS/pJ)

        self.word_to_freq_in_spam = {}
        self.word_to_freq_in_jam = {}

        self.train()

    def is_spam(self, email):
        words = [word.lower() for word in re.split('[.!?,:;]|\s', fl.read()) if len(word)>1 or word in ['I', 'i']]

        prob_spam_ratio = self.log_pS_div_pJ
        for word in words:
            prob_spam_ratio += log(self.word_to_freq_in_spam.get(word, self.spam_prob_for_unknown_word) /
                                    self.word_to_freq_in_jam.get(word, self.spam_prob_for_unknown_word))

        return prob_spam_ratio > 0

    def train(self):
        pass




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
    from os import getcwd, listdir
    from os.path import isfile, join

    filter = SpamFilter()

    # testing on jams:
    num_jams = 0
    num_predicted_jams = 0
    for dir_item in listdir(join(getcwd(), 'jam-test')):
        try:
            with open(dir_item, 'r') as jam_fl:
                num_jams += 1
                if not filter.is_spam(jam_fl.read()):
                    num_predicted_jams += 1
        except OSError:
            print('Cannot open ', dir_item)
            continue

    if num_jams == 0:
        print('Found no test jams.')
    else:
        print('Accuracy on JAM tests: %.3f' % (num_predicted_jams / num_jams)*100)


    # testing on spams:
    num_spams = 0
    num_predicted_spams = 0
    for dir_item in listdir(join(getcwd(), 'spam-test')):
        try:
            with open(dir_item, 'r') as spam_fl:
                num_spams += 1
                if filter.is_spam(spam_fl.read()):
                    num_predicted_spams += 1
        except OSError:
            print('Cannot open ', dir_item)
            continue

    if num_spams == 0:
        print('Found no test spams.')
    else:
        print('Accuracy on SPAM tests: %.3f' % (num_predicted_spams / num_spams)*100)
