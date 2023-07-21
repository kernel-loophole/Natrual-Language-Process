import glob
import os
from random import shuffle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Embedding, Flatten, LSTM
def pre_process_data(filepath):
  positive_path = os.path.join(filepath, 'pos')
  negative_path = os.path.join(filepath, 'neg')
  print(positive_path)
  print(negative_path)
  pos_label = 1
  neg_label = 0
  dataset = []
  for filename in glob.glob(os.path.join(positive_path, '*.txt')):
    with open(filename, 'r') as f:
      dataset.append((pos_label, f.read()))
  for filename in glob.glob(os.path.join(negative_path, '*.txt')):
    # print("processing the file====>",filename)
    with open(filename, 'r') as f:
      dataset.append((neg_label, f.read()))
      shuffle(dataset)
  return dataset
def collect_expected(dataset):
  expected = []
  for sample in dataset:
    expected.append(sample[0])
  return expected
def avg_len(data):
  total_len = 0
  for sample in data:
    total_len += len(sample[1])
  return total_len/len(data)
def clean_data(data):
  new_data = []
  VALID = 'abcdefghijklmnopqrstuvwxyz0123456789"\'?!.,:; '
  for sample in data:
    
    new_sample = []
    for char in sample[1].lower():
      if char in VALID:
        new_sample.append(char)
      else:
        new_sample.append('UNK')
    new_data.append(new_sample)
  return new_data

def char_pad_trunc(data, maxlen=1000):
  new_dataset = []
  for sample in data:
    if len(sample) > maxlen:
      new_data = sample[:maxlen]
    elif len(sample) < maxlen:
      pads = maxlen - len(sample)
      new_data = sample + ['PAD'] * pads  
    else:
      new_data = sample
    new_dataset.append(new_data)
  return new_dataset

def create_dicts(data):
  chars = set()
  for sample in data:
    chars.update(set(sample))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
  return char_indices, indices_char
def onehot_encode(dataset, char_indices, maxlen=1500):
  X = np.zeros((len(dataset), maxlen, len(char_indices.keys())))
  for i, sentence in enumerate(dataset):
    for t, char in enumerate(sentence):
      X[i, t, char_indices[char]] = 1
  return X

dataset = pre_process_data('dataset/train')
expected = collect_expected(dataset)
listified_data=clean_data(dataset)
# data_set_dict=create_dicts(listed_data)
common_length_data = char_pad_trunc(listified_data, maxlen=1000)
char_indices, indices_char = create_dicts(common_length_data)
encoded_data = onehot_encode(common_length_data, char_indices, 1000)
"""
A numpy array of length equal to the number of data
samples—each sample will be a number of tokens equal
to maxlen, and each token will be a one-hot encoded
vector of length equal to the number of characters
"""
"""
np array of shape (samples, tokens, encoding length)"""
# print(encoded_data.shape)

split_point = int(len(encoded_data)*.8)
x_train = encoded_data[:split_point]
y_train = expected[:split_point]
x_test = encoded_data[split_point:]
y_test = expected[split_point:]