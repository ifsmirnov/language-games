from pymorphy2 import MorphAnalyzer
import re

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


def create_bow(file_from, file_to, normalize=True):
    w = bag_of_words(file_from, normalize)
    print>>open(file_to, "w"), "\n".join(w).encode("utf8")
