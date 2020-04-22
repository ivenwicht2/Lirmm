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


    #word_counts = Counter(text)
    #sorted_vocab = dict((c, i) for i, c in enumerate(chars))
    #int_to_vocab = {k: w for k, w in enumerate(sorted_vocab)}
    #vocab_to_int = {w: k for k, w in int_to_vocab.items()}
    vocab_to_int = dict((c, i) for i, c in enumerate(chars))
    int_to_vocab = dict((i, c) for i, c in enumerate(chars))
    n_vocab = len(int_to_vocab)
    np.save("save/int_to_vocab",int_to_vocab)
    np.save("save/vocab_to_int",vocab_to_int)
    print('Vocabulary size', n_vocab)
    print("total charact : ", len(text))

    int_text = [vocab_to_int[w] for w in text]
    num_batches = int(len(int_text) / (seq_size * batch_size))
    in_text = int_text[:num_batches * batch_size * seq_size]
    out_text = np.zeros_like(in_text)
    out_text[:-1] = in_text[1:]
    out_text[-1] = in_text[0]
    in_text = np.reshape(in_text, (batch_size, -1))
    out_text = np.reshape(out_text, (batch_size, -1))
    return int_to_vocab, vocab_to_int, n_vocab, in_text, out_text



def get_batches(in_text, out_text, batch_size, seq_size):
    num_batches = np.prod(in_text.shape) // (seq_size * batch_size)
    for i in range(0, num_batches * seq_size, seq_size):
        yield in_text[:, i:i+seq_size], out_text[:, i:i+seq_size]