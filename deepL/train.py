from model import LSTM
import numpy as np 
from dataset import *
import torch 
import torch.nn as nn
from argparse import Namespace

flags = Namespace(
    seq_size=100,
    batch_size=64,
    embedding_size=256,
    lstm_size=256,
    gradients_norm=5,
    checkpoint_path='checkpoint',
    num_epochs = 200
)

def train():
    int_to_vocab, vocab_to_int, n_vocab, in_text = get_data_from_file( flags.batch_size, flags.seq_size)
    x_batch,y_batch = create_batch(in_text,flags.batch_size,flags.seq_size)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = LSTM(n_vocab, flags.seq_size,flags.embedding_size, flags.lstm_size).to(device)

    #optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.7)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_function = nn.CrossEntropyLoss()

    for e in range(flags.num_epochs):
        print(f'epoch #{e}: ',end="")
        batches = get_batches(x_batch,y_batch,flags.batch_size, flags.seq_size)
        (state_h_1, state_c_1),(state_h_2, state_c_2) = model.zero_state(flags.batch_size)
        state_h_1 = state_h_1.to(device)
        state_c_1 = state_c_1.to(device)
        state_h_2 = state_h_2.to(device)
        state_c_2 = state_c_2.to(device)
        
        for i,(x, y) in enumerate(batches):
            model.train()
            optimizer.zero_grad()
 

            x = torch.tensor(x , dtype=torch.int64).to(device)
            #print("x shape {} ".format(np.shape(x)))
            
            tmp = []
            for index,el in enumerate(y) :
                tmp.append(np.zeros(n_vocab))
                tmp[index][y[index]] = 1
            #print(y)
            y = tmp 
            y = torch.tensor(y , dtype=torch.int64).to(device)
            logits, (state_h_1, state_c_1),(state_h_2, state_c_2) = model(x, (state_h_1, state_c_1),(state_h_2, state_c_2))
            #print("logits shape {} , y shape {}".format(np.shape(logits),np.shape(y)))
            loss = loss_function(logits, y)

            state_h_1 = state_h_1.detach()
            state_c_1 = state_c_1.detach()
            state_h_2 = state_h_2.detach()
            state_c_2 = state_c_2.detach()

            loss_value = loss.item()

            loss.backward()
            _ = torch.nn.utils.clip_grad_norm_(model.parameters(), flags.gradients_norm)
            optimizer.step()
        print(f'batch #{i}:\tloss={loss.item():.10f}')
    return model 

if __name__ == "__main__":
    model = train()
    torch.save(model,'save/model')

