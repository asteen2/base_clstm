
import sys
sys.path.insert(1, "../code_development/")
import load_data as ld

import pickle
import numpy as np

def test_GetResults():
    testInput = pickle.load(open("data_testing/correctOneHotIn.pickle", "rb"))
    testCorrectOut = pickle.load(open("data_testing/correctOneHotOut.pickle", "rb"))

    getOneHotOut = ld.get_onehot(testInput, None, num_classes=3, seq_len=20)

#    print(testInput)
#    print(testCorrectOut)

    for x,y in zip(testCorrectOut,getOneHotOut):
        assert np.equal(x,y).all()
    #assert getOneHotOut[1].shape == testCorrectOut[1].shape
    #assert np.equal(getOneHotOut[1], testCorrectOut[1])

def test_CorrectDataType():
    testInput = pickle.load(open("data_testing/correctOneHotIn.pickle", "rb"))

    getOneHotOut = ld.get_onehot(testInput, None, num_classes=3, seq_len=20)

    assert type(getOneHotOut[0]) is np.ndarray
    assert type(getOneHotOut[1]) is np.ndarray
    # this test is written for get_onehot() with has_mask=False. If
    # has_mask=True, this third assertion will fail.
    assert getOneHotOut[2] is None
