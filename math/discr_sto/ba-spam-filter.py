def is_spam(fl_name):

    with open(fl_name, 'r') as f:
        import re

        words = re.split('[.]|\s', f.read())


if __name__ == "__main__":
    pass
