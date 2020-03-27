from model import LSTM
import numpy as np 
from dataset import data_import , prepare_sequence
import torch 
import torch.nn as nn

def train():
    data_batches , num_epochs , batch_size ,num_batchs , embedding_dim,hidden_dim , vocab = data_import()
    word2idx = np.load("save/word2idx.npy",allow_pickle='TRUE').item()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = LSTM(len(vocab), embedding_dim, hidden_dim).to(device)
    model.train()

    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5)
    loss_function = nn.MSELoss()

    for e in range(num_epochs):
        print(f'\n\nepoch #{e}:\n')
        
        for i,(sentence, tags) in enumerate(data_batches):
            model.zero_grad()

            hidden = (torch.zeros(1,1,hidden_dim).to(device),
                            torch.zeros(1,1,hidden_dim).to(device))
            model.hidden_cell1  = hidden
            model.hidden_cell2 = hidden

            x = prepare_sequence(sentence, word2idx,device)   
            #y = prepare_sequence(tags, word2idx,device)
            idx = [word2idx[w] for w in tags]
            tmp = [0 for _ in range(len(vocab))]
            tmp[idx[0]] = 1
            y = torch.tensor(tmp, dtype=torch.long,device=device)

            y_pred = model(x)
            loss = loss_function(y_pred.float(), y.float())
            loss.backward()
            optimizer.step()

            if i % 50 == 0:
                print(f'\tbatch #{i}:\tloss={loss.item():.10f}')

    return model 

if __name__ == "__main__":
    model = train()
    torch.save(model,'save/model2')

