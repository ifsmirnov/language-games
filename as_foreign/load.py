# -*- encoding: utf8 -*-
import pickle

""" Dict format:
name/
├— norm.freq       +  # frequency map of normalized words
├— raw_rev_3.ngram +  # 3-grams of reversed raw words; "big" ngrams
├— raw_rev_2.ngram +  # 2-grams of reversed raw words: "small" ngrams
├— ...

Full format is described in generate.py.
"""

def load_all(path_to_dict):
    if not path_to_dict.endswith("/"):
        path_to_dict += "/"

    try:
        return dict(
                freq=load_frequency_list(path_to_dict + "norm.freq"),
                ngram_small=load_ngrams(path_to_dict + "raw_rev_2.ngram"),
                ngram_big=load_ngrams(path_to_dict + "raw_rev_3.ngram"),
        )
    except Exception, e:
        print "Cannot load dictionary:", e


def load_ngrams(file_from):
    return pickle.load(open(file_from))


def load_frequency_list(file_from):
    return { word : idx for idx, word in enumerate(
            i.decode("utf8").split()[0] for i in open(file_from).readlines()
    )}
