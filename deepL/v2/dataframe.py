import re 
import numpy as np
import pandas as pd 
import torch 
from sklearn.utils import shuffle
import string 

def get_data_from_file(trainfilename,batch_size, seq_size) :
    
    raw_text = open(trainfilename, 'r', encoding='utf-8').read()
    raw_text = raw_text.lower()
    raw_text = raw_text.translate(str.maketrans('', '', string.punctuation))
    #raw_text = raw_text.split()
    raw_text =  [char for char in raw_text] 
    
    chars = sorted(list(set(raw_text)))
    #chars = list(set(raw_text))
    #print(chars)
    vocab_to_int = dict((c, i) for i, c in enumerate(chars))
    int_to_vocab = dict((i, c) for i, c in enumerate(chars))
    n_vocab = len(int_to_vocab)
    np.save("save/int_to_vocab",int_to_vocab)
    np.save("save/vocab_to_int",vocab_to_int)
    print('Vocabulary size', n_vocab)
    print("total charact : ", len(raw_text))


    n_chars = len(raw_text)
    n_vocab= len(chars)

    n_seq = int(((n_chars-1)/seq_size)-seq_size) 
    n_batch = int(n_seq/batch_size)
    print("batch ",n_batch)

    encode_X , encode_Y = [] , []

    for i in range(0,n_seq):
        tmp_X = raw_text[i:i+seq_size]
        tmp_Y = raw_text[i+seq_size]

        encode_X.append([vocab_to_int[el] for el in tmp_X])
        encode_Y.append(vocab_to_int[tmp_Y])



    return (encode_X,encode_Y) ,n_batch , n_vocab


def batch(seq,n_batch,batch_size,device) :
    X,Y = seq
    X, Y = shuffle(X, Y, random_state=0)
    X_tensor = torch.tensor(X).to(torch.int64).to(device)
    Y_tensor = torch.tensor(Y).to(torch.int64).to(device)
    #print(len(X_tensor),len(X_tensor)//batch_size,n_batch)
    #print(np.shape(X_tensor),n_batch,batch_size)
    for i in range(0,n_batch,batch_size) :
        batchX = X_tensor[i:i+batch_size]
        batchY = Y_tensor[i:i+batch_size]
        yield (batchX,batchY)

    