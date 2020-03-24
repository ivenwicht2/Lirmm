import torch
import torch.nn as nn
import torch.nn.functional as F

class LSTM(nn.Module) :
    def __init__(self,vocab_size, embedding_dim, hidden_dim):
        super(LSTM, self).__init__()
        self.hidden_dim = hidden_dim
        
        self.encoder = nn.Embedding(vocab_size, embedding_dim)

        self.lstm = nn.LSTM(embedding_dim, hidden_dim)

        self.decoder = nn.Linear(hidden_dim,vocab_size)




    def forward(self,sentence):
        x = self.encoder(sentence)
        x , _ = self.lstm(x.view(len(sentence), 1, -1))
        x = self.decoder(x)
        print(len(x))
        x = F.log_softmax(x, dim = 1)
        return x
