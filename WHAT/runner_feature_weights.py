from __future__ import division
from Methods.what import what
from Methods.guo_random import guo_random
from Utilities.model import generate_model
from Utilities.normalize import do_normalize_min_max, do_normalize_zscore
from Utilities.feature_weighting import add_feature_weights
import numpy as np
import os


def experiment2(filename, ret_val):
    mmre = []
    for _ in xrange(30):
        method = guo_random(filename)
        training_data, testing_data = method.generate_test_data(ret_val)
        assert(len(training_data[0]) == len(training_data[-1])), "Something is wrong"
        assert(len(testing_data[0]) == len(testing_data[-1])), "Something is wrong"
        mmre.append(generate_model(training_data, testing_data))

    print round(np.mean(mmre) * 100, 3), round(np.std(mmre) * 100, 3),


def experiment1(filename, normalize=None, feature_weights=False):
    if normalize is not None:
        name = filename.split('/')[-1]
        norm_filename = "./NData/zscore/norm_" + name

    mmre = []
    for _ in xrange(30):
        if feature_weights is True:
            filename = add_feature_weights(norm_filename)
        method = what(filename)
        training_data, testing_data = method.generate_test_data()
        assert(len(training_data[0]) == len(training_data[-1])), "Something is wrong"
        assert(len(testing_data[0]) == len(testing_data[-1])), "Something is wrong"
        mmre.append(generate_model(training_data, testing_data))

    print round(np.mean(mmre) * 100, 3), round(np.std(mmre) * 100, 3),
    return len(training_data[0])

if __name__ == "__main__":
    files = ["./Data/"+f for f in os.listdir("./Data/") if ".csv" in f]
    # files = ["./Data/BDBC_AllMeasurements.csv"]
    # import pdb
    # pdb.set_trace()
    for file in files:
        print file,
        ret_val = experiment1(file, normalize=do_normalize_zscore, feature_weights=True)
        experiment2(file, ret_val)
        print