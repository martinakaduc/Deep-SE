from prepare_data import *
import _pickle as cPickle
import os
import sys

paths = os.listdir("../NCE/bestModels")
paths = list(filter(lambda x: x[-5:] == ".hdf5" and "dim50" in x and sys.argv[1] in x, paths))
paths = [x[:-5] for x in paths]

for path in paths:
    w = load_weight(path)

    f = open("../inference/emb_weights/" + path + ".pkl", "wb")
    cPickle.dump(w, f, -1)
    f.close()
