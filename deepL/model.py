import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np 

class LSTM(nn.Module) :
    def __init__(self,vocab_size, embedding_dim, hidden_dim):
        super(LSTM, self).__init__()
        self.vocab = vocab_size
        self.hidden_cell1 = None
        self.hidden_cell2 = None

        self.encoder = nn.Embedding(vocab_size, embedding_dim)

        self.lstm = nn.LSTM(embedding_dim, hidden_dim)
        self.lstm2 = nn.LSTM(hidden_dim,hidden_dim)

        self.decoder = nn.Linear(in_features=hidden_dim,out_features=vocab_size,bias=True)


    def forward(self,sentence):
        x = self.encoder(sentence)
        x , self.hidden_cell1 = self.lstm(x.view(len(sentence), 1, -1),self.hidden_cell1)
        x , self.hidden_cell2 = self.lstm2(x,self.hidden_cell2)
        x = self.decoder(x.view(len(sentence), -1))
        x = F.log_softmax(x, dim = 1)
        return x[-1]
