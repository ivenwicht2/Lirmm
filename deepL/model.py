import torch
import torch.nn as nn

class LSTM(nn.Module) :
    def __init__(self,vocab_size, word_size, sequence_len, batch_size, hidden_dim):
        super().__init__()

        self.seq_len = sequence_len
        self.batch_size = batch_size
        self.hidden_dim = hidden_dim
        self.num_layers = 2

        self.h_0 = None
        self.c_0 = None


        self.encoder = nn.Embedding(vocab_size, word_size)

        self.lstm = nn.LSTM(input_size=word_size, hidden_size=self.hidden_dim,
							num_layers=self.num_layers, batch_first=True, dropout=0.2)
        self.lstm2 = nn.LSTM(input_size=self.hidden_dim, hidden_size=self.hidden_dim,
							num_layers=self.num_layers, batch_first=True, dropout=0.2)
        self.lstm3 = nn.LSTM(input_size=self.hidden_dim, hidden_size=self.hidden_dim,
							num_layers=self.num_layers, batch_first=True, dropout=0.2)
        self.decoder = nn.Linear(self.hidden_dim,vocab_size)

	
    def reset_hidden(self):
	    self.h_0 = torch.zeros(self.num_layers, self.batch_size, self.hidden_dim)
	    self.c_0 = torch.zeros(self.num_layers, self.batch_size, self.hidden_dim)
	    self.h_1 = torch.zeros(self.num_layers, self.batch_size, self.hidden_dim)
	    self.c_1 = torch.zeros(self.num_layers, self.batch_size, self.hidden_dim)
	    self.h_2 = torch.zeros(self.num_layers, self.batch_size, self.hidden_dim)
	    self.c_2 = torch.zeros(self.num_layers, self.batch_size, self.hidden_dim)
        
    def forward(self,x):
        x = self.encoder(x)
        x , (self.h_0, self.c_0) = self.lstm(x)
        x , (self.h_1, self.c_1) = self.lstm2(x)
        x , (self.h_2, self.c_2) = self.lstm3(x)
        x = self.decoder(x[:, -1, :])
        return x
