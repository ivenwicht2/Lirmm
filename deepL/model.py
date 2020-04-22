import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np 

class LSTM(nn.Module) :
    def __init__(self,vocab_size, seq_size, embedding_dim, hidden_dim):
        super(LSTM, self).__init__()
        self.vocab = vocab_size
        self.hidden_size = hidden_dim
        self.seq_size = seq_size

        self.encoder = nn.Embedding(vocab_size, embedding_dim)

        self.lstm = nn.LSTM(embedding_dim, hidden_dim , batch_first=True )
        self.dropout_1 = nn.Dropout(p=0.2, inplace=False)
        self.lstm2 = nn.LSTM(embedding_dim, hidden_dim , batch_first=True )
        self.dropout_2 = nn.Dropout(p=0.2, inplace=False)
        self.decoder = nn.Linear(in_features=hidden_dim,out_features=vocab_size)
        self.activation = nn.Softmax(dim=0)
    def zero_state(self, batch_size):
        return (
                (torch.zeros(1, batch_size, self.hidden_size),
                torch.zeros(1, batch_size, self.hidden_size)), 

                (torch.zeros(1, batch_size, self.hidden_size),
                torch.zeros(1, batch_size, self.hidden_size)),                
                )

    def forward(self,sentence,prev_state_1,prev_state_2):
        #print("sentence shape ",np.shape(sentence))
        #print("prev shape ",np.shape(prev_state_1))
        x = self.encoder(sentence)
        x , hidden_cell_1 = self.lstm(x,prev_state_1)
        x = self.dropout_1(x)
        x , hidden_cell_2 = self.lstm2(x,prev_state_2)
        x = self.dropout_2(x)
        x = self.decoder(x)
        x = F.log_softmax(x, dim=1)
        return x , hidden_cell_1,hidden_cell_2
