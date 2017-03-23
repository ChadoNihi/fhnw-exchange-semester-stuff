# I followed this naive Bayes classifier - http://www.cs.ubbcluj.ro/~gabis/DocDiplome/Bayesian/000539771r.pdf
from math import log # logarithm to overcome rounding errors of small numbers
from os import getcwd, listdir
from os.path import isfile, join
import re

class SpamFilter(object):
    def __init__(self):
        self.spam_prob_for_unknown_word = 0.5

        self.pS = None
        self.pJ = None
        self.log_pS_div_pJ = None

        self.word_to_freq_in_spam = {}
        self.word_to_freq_in_jam = {}

        self.train()

    def is_spam(self, email):
        # TODO: preprocess_email(email): to lower; replace words with stems, normalize URLs, numbers, etc.
        words = [word.lower() for word in re.split('[.!?,:;]|\s', fl.read()) if len(word)>1 or word in ['I', 'i']]

        prob_spam_ratio = self.log_pS_div_pJ
        for word in words:
            prob_spam_ratio += log(self.word_to_freq_in_spam.get(word, self.spam_prob_for_unknown_word) /
                                    self.word_to_freq_in_jam.get(word, self.spam_prob_for_unknown_word))

        return prob_spam_ratio > 0

    def train(self):
        # first, train on jam
        num_jams = 0
        word_to_count = {}
        path_to_jam_train_files = join(getcwd(), 'jam-train')
        for dir_item in listdir(path_to_jam_train_files):
            try:
                with open(join(path_to_jam_train_files, dir_item), 'r') as jam_fl:
                    num_jams += 1

                    words = [word.lower() for word in re.split('[.!?,:;]|\s', jam_fl.read()) if len(word)>1 or word in ['I', 'i']]
                    for word in words:
                        word_to_count[word] = word_to_count.setdefault(word, 0) + 1

            except OSError:
                print('Cannot open ', dir_item)
                continue

        for word, count in word_to_count.items():
            self.word_to_freq_in_jam[word] = count / num_jams


        # repeat for spam
        num_spams = 0
        word_to_count = {}
        path_to_spam_train_files = join(getcwd(), 'spam-train')
        for dir_item in listdir(path_to_spam_train_files):
            try:
                with open(join(path_to_spam_train_files, dir_item), 'r') as spam_fl:
                    num_spams += 1

                    words = [word.lower() for word in re.split('[.!?,:;]|\s', spam_fl.read()) if len(word)>1 or word in ['I', 'i']]
                    for word in words:
                        word_to_count[word] = word_to_count.setdefault(word, 0) + 1

            except OSError:
                print('Cannot open ', dir_item)
                continue

        try:
            self.pS = num_spams / (num_spams+num_jams)
            self.pJ = num_jams / (num_spams+num_jams)
            self.log_pS_div_pJ = log(self.pS/self.pJ)
        except ZeroDivisionError:
            print('Found no train examples. Maybe you use evil \'ham\' instead of lovely \'jam\'?')
            return

        for word, count in word_to_count.items():
            self.word_to_freq_in_spam[word] = count / num_spams

if __name__ == "__main__":
    filter = SpamFilter()

    # testing on jams:
    num_jams = 0
    num_predicted_jams = 0
    path_to_jam_test_files = join(getcwd(), 'jam-test')
    for dir_item in listdir(path_to_jam_test_files):
        try:
            with open(join(path_to_jam_test_files, dir_item), 'r') as jam_fl:
                num_jams += 1
                if not filter.is_spam(jam_fl.read()):
                    num_predicted_jams += 1
        except OSError:
            print('Cannot open ', dir_item)
            continue

    if num_jams == 0:
        print('Found no test jams. Maybe you use evil \'ham\' instead of lovely \'jam\'?')
    else:
        print('Accuracy on JAM tests: %.3f' % (num_predicted_jams / num_jams)*100)


    # testing on spams:
    num_spams = 0
    num_predicted_spams = 0
    path_to_spam_test_files = join(getcwd(), 'spam-test')
    for dir_item in listdir(path_to_spam_test_files):
        try:
            with open(join(path_to_spam_test_files, dir_item), 'r') as spam_fl:
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
