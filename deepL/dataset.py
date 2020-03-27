import numpy as np 
import pandas as pd 
import random
import torch 

def data_import() :
    data = ""

    with open('wikipediaTXT.txt', 'r') as fh:
        for index,line in enumerate(fh):
            data += line
            if index == 50000 : break             
    words = data

    vocab = set(words)
    print(f'\nvocab size: {len(vocab)}')

    word2idx = {w:idx for idx, w in enumerate(vocab)}
    idx2word = {idx:w for w, idx in word2idx.items()}

    sequence_len = 30
    batch_size = 100
    embedding_dim =400
    hidden_dim = 100
    num_epochs = 2
    
    data_batches = []
    for i in range(len(words) - sequence_len - 1): 
        data = [x for x in words[i: i + sequence_len]]
        target = words[i + sequence_len]

        data_batches.append([data, target])

    num_batchs = np.ceil(len(data_batches) / batch_size).astype(np.int)
    random.shuffle(data_batches)
    print(f'\nnumber of batches: {num_batchs}')
    print("number of epochs : ", num_epochs)
    np.save("save/word2idx",word2idx)
    np.save("save/idx2word",idx2word)
    return data_batches , num_epochs , batch_size , num_batchs , embedding_dim ,hidden_dim, vocab



def prepare_sequence(seq, to_ix,device):
    idxs = [to_ix[w] for w in seq]
    return torch.tensor(idxs, dtype=torch.long,device=device)