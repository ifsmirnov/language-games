from pymorphy2 import MorphAnalyzer
import re
import pickle

morph = MorphAnalyzer()

def words_from_line(line, normalize=True):
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


def words_from_file(filename, normalize=True):
    """Return list of russian word from file, probably in normal form"""

    res = []
    cnt = 0
    for line in open(filename).readlines():
        if cnt % 10 == 0:
            print cnt
        cnt += 1
        res += words_from_line(line, normalize)
    return res


def generate_bag_of_words(file_from, file_to, normalize=True):
    """Save [normalized] words from xml/text from file_from to file to"""

    w = bag_of_words(file_from, normalize)
    print>>open(file_to, "w"), "\n".join(w).encode("utf8")


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
    uprint(res)
    pickle.dump(res, open(file_to, "w"))


def generate_frequency_list(file_from, file_to):
    """Write words from file_from to file_to ordered by frequency, desc"""

    words = [w.decode("utf8").strip() for w in open(file_from).readlines()]
    cnt = {}
    for word in words:
        if word not in cnt:
            cnt[word] = 1
        else:
            cnt[word] += 1
    sorted_words = sorted(((i[1], i[0]) for i in cnt.items()), reverse=True)
    print sorted_words[0]
    to = open(file_to, "w")
    for i in sorted_words:
        print>>to, i[1].encode("utf8"), i[0]
