from model import LSTM
import numpy as np 
from dataset import data_import
import torch 

def train():
    data_batches , num_epochs , batch_size ,num_batchs , sequence_len , word_size , vocab = data_import()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = LSTM(len(vocab), word_size, sequence_len, batch_size, 50).to(device)
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

    num_epochs = 2

    for e in range(num_epochs):
        print(f'\n\nepoch #{e}:\n')
        model.reset_hidden()
        
        for i in range(num_batchs):
            batch = data_batches[i * batch_size: (i+1) * batch_size]
            x = torch.tensor([b[0] for b in batch], device=device)
            y = torch.tensor([b[1] for b in batch], device=device)

            y_pred = model(x)

            loss = criterion(y_pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if i % 50 == 0:
                print(f'\tbatch #{i}:\tloss={loss.item():.10f}')

    return model 

if __name__ == "__main__":
    model = train()
    torch.save(model,'save/model2')