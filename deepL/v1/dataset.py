import numpy as np 
import random
import torch 
from collections import Counter
import string

def get_data_from_file(batch_size, seq_size) :
    filename = "corpus.txt"
    raw_text = open(filename, 'r', encoding='utf-8').read()
    text = raw_text.lower()
    #text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.split()
    
    chars = sorted(list(set(text)))


    vocab_to_int = dict((c, i) for i, c in enumerate(chars))
    int_to_vocab = dict((i, c) for i, c in enumerate(chars))
    n_vocab = len(int_to_vocab)
    np.save("save/int_to_vocab",int_to_vocab)
    np.save("save/vocab_to_int",vocab_to_int)
    print('Vocabulary size', n_vocab)
    print("total charact : ", len(text))

    int_text = np.array([vocab_to_int[w] for w in text])
    return int_to_vocab, vocab_to_int, n_vocab,int_text


def create_batch(array,batch_size,seq_size):
    num_batches = int(len(array) / (seq_size * batch_size))
    array = array[:num_batches * batch_size * seq_size]
    x_batch = np.array(np.split(array, int(len(array) / seq_size)      ))
    y_batch = x_batch[:,-1]
    x_batch = np.delete(x_batch, np.s_[::2], 1)
    print("x shape {} , y shape {} ".format(np.shape(x_batch),np.shape(y_batch)))
    return x_batch,y_batch
    

def get_batches(x,y ,batch_size, seq_size):
    num_batches = len(x)
    for i in range(0, num_batches,batch_size):
        yield x[i:i+batch_size], y[i:i+batch_size]