# -*- encoding: utf8 -*-
#!/usr/bin/python

# a = '    <p>— Понимаешь, у них под иглами тучи всяких паразитов, а сами они до них добраться не могут. Для них почесывание — первейшее дело. А ну-ка, приятель, подставляй второе ухо. За ушами у них зудит сильнее всего. Сейчас дочешу, и двинемся дальше.</p> '

from pymorphy2 import MorphAnalyzer

from ngrams import *
from alphabet import *
from random_words import *
from generate import *
from load import *
from utils import *

FILENAME = "Garrison_Vsya-Stalnaya-Krysa-Tom-1.371445.fb2"

data = load_all("mydict")
if not data:
    exit(1)

tokens = extract_typed_tokens(open("input.txt").readline().strip())

print similar_phrase(
        tokens,
        data["ngram_big"],
        data["ngram_small"],
        lambda w: word_is_frequent(w, 500, data["freq"])
)
