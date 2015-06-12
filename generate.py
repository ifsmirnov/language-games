# -*- encoding: utf8 -*-
from pymorphy2 import MorphAnalyzer
import re
import pickle
from os import mkdir
from sys import stdout
from time import clock

from alphabet import RUSSIAN_ALPHABET
from ngrams import ngram_frequency

flush = stdout.flush

"""
words_from_line(line, normalize=False)
words_from_file(filename, normalize=False)

generate_bag_of_words(file_from, file_to, normalize=False)
generate_reversed_words(file_from, file_to)
generate_ngrams(file_from, file_to, n)
generate_frequency_list(file_from, file_to)
"""

""" Dict format:
name/
├— source.text        # source text, unchanged
├— raw.data           # raw words
├— norm.data          # normalized words
├— raw_rev.data       # raw words, reversed
├— norm.freq       +  # frequency map of normalized words
├— raw_rev_3.ngram +  # 3-grams of reversed raw words; "big" ngrams
├— raw_rev_2.ngram +  # 2-grams of reversed raw words: "small" ngrams

Those marked with '+' are useful for the end-user.
"""

def generate_all(path_to_book, path_to_dict):
    try:
        mkdir(path_to_dict)
    except OSError:
        raise RuntimeError("Dictionary already exists")

    if not path_to_dict.endswith("/"):
        path_to_dict += "/"

    timestamp = clock()
    initial_timestamp = timestamp

    def log_time():
        t = clock()
        print "%d ms" % ((t - timestamp) * 1000,)
        return t

    try:
        print "Copying initial book...",
        open(path_to_dict + "source.text", "w").write(open(path_to_book).read())
        print "OK",; timestamp = log_time()

        print "Generating raw words...",; flush()
        n = generate_bag_of_words(path_to_book, path_to_dict + "raw.data")
        print "OK %d words," % n,; timestamp = log_time()

        print "Generating normalized words (takes about a minute)...",; flush()
        generate_bag_of_words(path_to_book, path_to_dict + "norm.data", normalize=True, total=n)
        print "OK",; timestamp = log_time()

        print "Generating reversed raw words...",; flush()
        generate_reversed_words(path_to_dict + "raw.data", path_to_dict + "raw_rev.data")
        print "OK",; timestamp = log_time()

        print "Generating normalized words frequency...",; flush()
        n = generate_frequency_list(path_to_dict + "norm.data", path_to_dict + "norm.freq")
        print "OK %d words," % n,; timestamp = log_time()

        print "Generating 2-grams...",; flush()
        generate_ngrams(path_to_dict + "raw_rev.data", path_to_dict + "raw__rev_2.ngram", 2)
        print "OK",; timestamp = log_time()

        print "Generating 3-grams...",; flush()
        generate_ngrams(path_to_dict + "raw_rev.data", path_to_dict + "raw_rev_3.ngram", 3)
        print "OK",; timestamp = log_time()

        print "OK, dictionary '%s' generated in %d ms" % (path_to_dict[:-1], (clock() - initial_timestamp) * 1000)

        return True

    except Exception, e:
        print
        print "Failed to generate dictionary:",
        print e.message
        return False


morph = MorphAnalyzer()

def words_from_line(line, normalize=False):
    """Return list of russian words from a line of xml text, probably in normal form"""

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


def words_from_file(filename, normalize=False, total=None):
    """Return list of russian word from file, probably in normal form"""

    res = []
    cnt = 0
    last_percent = 0
    for line in open(filename).readlines():
        t = words_from_line(line, normalize)
        cnt += len(t)
        res += t
        if total is not None:
            percent = cnt * 100 / total
            if percent > last_percent:
                last_percent = percent
                if percent % 10 == 0:
                    print "%d%%" % percent,; flush()

    return res


def generate_bag_of_words(file_from, file_to, normalize=False, total=None):
    """Save [normalized] words from xml/text from file_from to file to

    Returns number of words"""

    w = words_from_file(file_from, normalize, total=total)
    print>>open(file_to, "w"), "\n".join(w).encode("utf8")

    return len(w)


def generate_reversed_words(file_from, file_to):
    """Read words from file_from and write them to file_to, reversed"""

    to = open(file_to, "w")
    for word in open(file_from).readlines():
        print>>to, word.decode("utf8").strip()[::-1].encode("utf8")


def generate_ngrams(file_from, file_to, n):
    """Read words from file_from and write pickled n-gram frequency to file_to"""

    res = ngram_frequency(
            [i.strip().decode("utf8") for i in open(file_from).readlines()],
            n)
    pickle.dump(res, open(file_to, "w"))


def generate_frequency_list(file_from, file_to):
    """Write words from file_from to file_to ordered by frequency, desc

    Returns number of distinct words"""

    words = [w.decode("utf8").strip() for w in open(file_from).readlines()]
    cnt = {}
    for word in words:
        if word not in cnt:
            cnt[word] = 1
        else:
            cnt[word] += 1
    sorted_words = sorted(((i[1], i[0]) for i in cnt.items()), reverse=True)
    to = open(file_to, "w")
    for i in sorted_words:
        print>>to, i[1].encode("utf8"), i[0]

    return len(sorted_words)
