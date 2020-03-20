import numpy as np 
import pandas as pd 
import random

def data_import() :
    df = pd.read_csv("88milSMS_88522.csv",sep=",",encoding = "ISO-8859-1")
    data = ""
    for index, text in df.iterrows() :
        data += str(text["SMS_ANON"])

    words = data.split()

    vocab = set(words)
    print(f'\nvocab size: {len(vocab)}')

    word2idx = {w:idx for idx, w in enumerate(vocab)}
    idx2word = {idx:w for w, idx in word2idx.items()}

    sequence_len = 30
    batch_size = 50
    word_size = 20
    num_epochs = 2

    data_batches = []
    for i in range(len(words) - sequence_len - 1): 
        data = [word2idx[x] for x in words[i: i + sequence_len]]
        target = word2idx[words[i + sequence_len]]

        data_batches.append([data, target])

    num_batchs = np.ceil(len(data_batches) / batch_size).astype(np.int)
    random.shuffle(data_batches)
    print(f'\nnumber of batches: {num_batchs}')
    print("number of epochs : ", num_epochs)
    return data_batches , num_epochs , batch_size , num_batchs , sequence_len , word_size , vocab