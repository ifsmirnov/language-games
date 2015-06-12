import pprint
from random import randint

from alphabet import *


def create_nd_array(dims, default=None):
    """Create N-dimensional array A[dims[0]]...[dims[n-1]]"""

    if len(dims) == 1:
        return [default] * dims[0]
    return [create_nd_array(dims[1:], default) for i in range(dims[0])]


def uprint(obj):
    """Pretty-print any object with unicode unescaped"""

    print pprint.pformat(obj).decode('unicode-escape')


def weighted_choice(items, total=None):
    """Given a list [(item, weight), ...], select random item according to weight"""

    if type(items) == enumerate:
        items = [i for i in items] # can't iterate over enumerate twice

    if total is None:
        total = sum(item[1] for item in items)

    # if last ngram occurs only at the end of the word we should generate
    # next character anyway
    if total == 0:
        return None
        return choice(items)[0]

    x = randint(0, total - 1)
    for item in items:
        if x < item[1]:
            return item[0]
        x -= item[1]

    raise RuntimeError("total is incorrect or all weights are zero")


def extract_typed_tokens(line):
    """Given a string, parse it into form [(is_rus (bool), token)...]"""

    if type(line) == str:
        line = line.decode("utf8")

    if len(line) == 0:
        return []

    tokens = []
    cur_token = ""
    is_rus = False
    for c in line:
        c_is_rus = c in RUSSIAN_ALPHABET
        if len(cur_token) == 0 or is_rus == c_is_rus:
            is_rus = c_is_rus
            cur_token += c
        else:
            tokens.append((is_rus, cur_token))
            cur_token = c
            is_rus = c_is_rus
    return tokens + [(is_rus, cur_token)]


