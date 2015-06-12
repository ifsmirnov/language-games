import pickle

def load_ngrams(file_from):
    return pickle.load(open(file_from))


def load_frequency_list(file_from):
    return { word : idx for idx, word in enumerate(
            i.decode("utf8").split()[0] for i in open(file_from).readlines()
    )}
