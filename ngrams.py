from alphabet import *

def ngram_frequency(word_list, n):
    """Return n-dim array where a[c1]...[cn] = number of c1..cn ngram occurrences"""

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


def as_dict(ngrams):
    """Given ngram array, return a dictionary { "ngram" : frequency }"""

    if type(ngrams) == int:
        return { "" : ngrams }
    res = {}
    for c in range(33):
        for word, count in as_dict(ngrams[c]).items():
            res[RUSSIAN_ALPHABET[c] + word] = count
    return res


def access_ngram(obj, word):
    """Helper for accessing multidimensional array with russian char indexing"""

    for c in word:
        obj = obj[rus_char_index(c)]
    return obj
