# -*- encoding: utf8 -*-
#!/usr/bin/python

# a = '    <p>— Понимаешь, у них под иглами тучи всяких паразитов, а сами они до них добраться не могут. Для них почесывание — первейшее дело. А ну-ка, приятель, подставляй второе ухо. За ушами у них зудит сильнее всего. Сейчас дочешу, и двинемся дальше.</p> '

import re
from pymorphy2 import MorphAnalyzer
import pprint
import pickle
from random import randint, choice

FILENAME = "Garrison_Vsya-Stalnaya-Krysa-Tom-1.371445.fb2"

RUSSIAN_ALPHABET =\
    "".join(map(unichr, range(1072, 1072 + 32))) + u'ё' +\
    "".join(map(unichr, range(1040, 1040 + 32))) + u'Ё';


def rus_char_index(c):
    try:
        return RUSSIAN_ALPHABET.index(c) - 33
    except:
        return -1


def create_nd_array(dims, default=None):
    if len(dims) == 1:
        return [default] * dims[0]
    return [create_nd_array(dims[1:], default) for i in range(dims[0])]


def uprint(obj):
    print pprint.pformat(obj).decode('unicode-escape')


morph = MorphAnalyzer()

def get_words(line, normalize=True):
    word_list = re.sub("<.*?>", " ", line).split()
    res = []
    for word in word_list:
        word = word.decode("utf8")
        word = re.sub("[^0-9%s-]" % RUSSIAN_ALPHABET, "", word)
        if word:
            if normalize:
                res.append(morph.parse(word)[0].normal_form)
            else:
                res.append(word.lower())
    return res


def bag_of_words(filename, normalize=True):
    res = []
    cnt = 0
    for line in open(filename).readlines():
        if cnt % 10 == 0:
            print cnt
        cnt += 1
        res += get_words(line, normalize)
    return res


def create_bow(file_from, file_to, normalize=True):
    w = bag_of_words(file_from, normalize)
    print>>open(file_to, "w"), "\n".join(w).encode("utf8")


def ngram_frequency(word_list, n):
    freq = create_nd_array([33] * n, 0)
    for word in word_list:
        idx = [rus_char_index(c) for c in word]
        if -1 in idx:
            continue
        ngrams = [ idx[i:i+n] for i in range(len(word) - n + 1)]
        for ngram in ngrams:
            obj = freq
            for c in ngram[:-1]:
                obj = obj[c]
            obj[ngram[-1]] += 1
    return freq


def access_ngram(obj, word):
    for c in word:
        obj = obj[rus_char_index(c)]
    return obj


def as_dict(ngrams):
    if type(ngrams) == int:
        return { "" : ngrams }
    res = {}
    for c in range(33):
        for word, count in as_dict(ngrams[c]).items():
            res[RUSSIAN_ALPHABET[c] + word] = count
    return res


def generate_ngrams(file_from, file_to, n):
    res = ngram_frequency(
            [i.strip().decode("utf8") for i in open(file_from).readlines()],
            n)
    uprint(res)
    pickle.dump(res, open(file_to, "w"))


def weighted_choice(items, total=None):
    if type(items) == enumerate:
        items = [i for i in items] # can't iterate over enumerate twice

    if total is None:
        total = sum(item[1] for item in items)

    # if last ngram occurs only at the end of the word we should generate
    # next character anyway
    if total == 0:
        return choice(items)[0]

    x = randint(0, total - 1)
    for item in items:
        if x < item[1]:
            return item[0]
        x -= item[1]

    raise RuntimeError("total is incorrect or all weights are zero")


def random_word(n, ngram, prev_ngram):
    word = weighted_choice(as_dict(prev_ngram).items())
    last = word
    for __ in range(n - len(word)):
        c = RUSSIAN_ALPHABET[weighted_choice(
                enumerate(access_ngram(ngram, last))
            )]
        word += c
        last = last[1:] + c
    return word

a = [pickle.load(open("raw_%d.ngram" % i)) for i in range(1, 5)]
for i in range(len(a) - 1):
    for j in range(5):
        print random_word(10, a[i+1], a[i])
    print
