# -*- encoding: utf8 -*-

RUSSIAN_ALPHABET =\
    "".join(map(unichr, range(1072, 1072 + 32))) + u'ё' +\
    "".join(map(unichr, range(1040, 1040 + 32))) + u'Ё';


def rus_char_index(c):
    try:
        return RUSSIAN_ALPHABET.index(c) - 33
    except:
        return -1
