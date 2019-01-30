from numpy.random import seed
seed(1)
from tensorflow import set_random_seed
set_random_seed(2)

import numpy as np
#from keras.models import Sequential
#from keras.layers import LSTM, Masking, Dense,  Bidirectional, Dropout, MaxPooling1D, Conv1D, Activation
#from keras.optimizers import Adam

from load_data import load_csv, get_onehot
from ml_logging import Logger
from model_templates import original_blstm, dna_blstm




is_dna_data = True

num_classes = 30
num_letters = 4 if is_dna_data else 26
sequence_length = 4500
logger = Logger('blstm_dna_conv3_4500')
save_path = '../models/blstm_dna_conv3_4500.h5'
data_dir = '/mnt/data/computervision/dna_train80_val10_test10'

model = dna_blstm(num_classes, num_letters, sequence_length)




model.summary()

train_data = load_csv(data_dir + '/train.csv')
print len(train_data)
val_data = load_csv(data_dir + '/validation.csv', divide=4 if is_dna_data else 1)
val_x, val_y = get_onehot(val_data, None, seq_len=sequence_length, is_dna_data=is_dna_data)
print len(val_data)

num_episodes = 40000
for i in range(num_episodes):
        x, y = get_onehot(train_data, 500, seq_len=sequence_length, is_dna_data=is_dna_data)
        print i
        print model.train_on_batch(x, y)
        if (i % 2000 == 0) or i == num_episodes - 1:

                [loss, acc] = model.evaluate(val_x, val_y, batch_size=500)
                print loss, acc
                logger.record_val_acc(i, acc)

                model.save(save_path)
                print 'saved to ' + save_path
del train_data

pred = model.predict(val_x, batch_size=500).argmax(axis=-1)
logger.confusion_matrix(val_data, pred)
logger.length_plot(val_data, pred)
logger.save()

del val_data, val_x, val_y

test_data = load_csv(data_dir + '/test.csv', divide=4 if is_dna_data else 1)
test_x, test_y = get_onehot(test_data, None, seq_len=sequence_length, is_dna_data=is_dna_data)
print "test accuracy: ", model.evaluate(test_x, test_y, batch_size=500)
