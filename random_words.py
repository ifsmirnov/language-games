# -*- encoding: utf8 -*-

from utils import weighted_choice
from ngrams import access_ngram, as_dict
from alphabet import *

def random_word(n, ngram, prev_ngram, prefix=None):
    """Generate random word of length n with given prefix

    ngram -- ngram frequency array of depth k,
    prev_ngram -- array of depth k-1"""

    def init():
        if prefix:
            return prefix
        return weighted_choice(as_dict(prev_ngram).items())


    def depth():
        c = 0
        obj = prev_ngram
        while type(obj) == list:
            c, obj = c + 1, obj[0]
        return c


    FORBIDDEN_ENDINGS = u"ъыь"


    word = init()
    k = depth()
    iters_left = 100
    while len(word) != n:
        iters_left -= 1
        if iters_left == 0:
            # if the word with given prefix cannot be generated
            # we generate fully random word
            word = random_word(n, ngram, prev_ngram)
            break
        idx = weighted_choice(
                enumerate(access_ngram(ngram, word[-k:]))
            )
        if idx is None or (
                len(word) == n-1 and RUSSIAN_ALPHABET[idx] in FORBIDDEN_ENDINGS):
            if len(word) <= k + 1:
                word = init()
            else:
                word = word[:-2]
        else:
            word += RUSSIAN_ALPHABET[idx]
    return word


def random_similar_word(word, ngram, prev_ngram):
    """Generate random word similar to the given one.

    Ending and capitalization are preserved"""

    def get_len(len):
        if len < 3:
            return len
        if len < 6:
            return 2
        return 3

    if type(word) == str:
        word = word.decode("utf8")

    capitals = [c.isupper() for c in word]

    word = word.replace(u'ё', u'е').replace(u'Ё', u'Е')

    new_word = random_word(
            len(word),
            ngram,
            prev_ngram,
            word[-get_len(len(word)):][::-1]
    )[::-1]

    return "".join(cap and c.upper() or c for c, cap in zip(new_word, capitals))


def similar_phrase(tokens, ngram, prev_ngram, allowed):
    """Substitute some words of the given phrase with similar random ones.

    Tokens -- array of form [(is_rus, token), ...].
    allowed(word) returns true for words not to be substituted (in normal form)"""

    res = ""
    for is_rus, token in tokens:
        if is_rus:
            if allowed(token):
                res += token
            else:
                res += random_similar_word(token, ngram, prev_ngram)
        else:
            res += token
    return res
