from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseNotAllowed

import sys
sys.path.insert(0, '/home/ifsmirnov/projects')

from as_foreign import *
import as_foreign

from time import time
import random

import traceback

def index(request):
    return render(request, "as_foreign_web/index.html", {})

last_request_time = {}

def text(request):
    try:
        if "seed" in request.POST:
            seed = int(request.POST["seed"])
        else:
            seed = None

        global last_request_time
        if time() - last_request_time.get(seed, 0) < 1.9:
            return HttpResponse("")
        last_request_time[seed] = time()

        random.seed(seed)

        data = load_all('/home/ifsmirnov/projects/as_foreign/mydict')
        tokens = extract_typed_tokens(request.POST["data"])

        top_k = int(request.POST.get("top_k", 0))

        res = similar_phrase(
                tokens,
                data['ngram_big'],
                data['ngram_small'],
                lambda w: word_is_frequent(w, top_k, data['freq'])
        ).encode("utf8")

        return HttpResponse(res)

    except Exception, e:
        print e
        traceback.print_exc()
        return HttpResponse("cannot generate phrase")
        
