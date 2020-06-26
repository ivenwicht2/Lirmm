from model import LSTM
import numpy as np 
from dataframe import *
import torch 
import torch.nn as nn
from argparse import Namespace
from tools import accuracy, stream, pred
#import matplotlib.pyplot as plt 

flags = Namespace(
    seq_size=100,
    trainfile = "corpus2.txt",
    batch_size=20,
    embedding_size=256,
    lstm_size=256,
    gradients_norm=5,
    num_epochs = 91,
    lr = 0.001
)

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    seq  , n_batch   , n_vocab = get_data_from_file(flags.trainfile,flags.batch_size, flags.seq_size)


    model = LSTM(n_vocab, flags.seq_size,flags.embedding_size, flags.lstm_size).to(device)


    #optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.7)
    optimizer = torch.optim.Adam(model.parameters(), lr=flags.lr)
    loss_function = nn.CrossEntropyLoss()

    total_acc = []
    total_loss = []

    for e in range(flags.num_epochs):
        (state_h_1, state_c_1),(state_h_2, state_c_2) = model.zero_state(flags.batch_size)
        state_h_1 = state_h_1.to(device)
        state_c_1 = state_c_1.to(device)
        state_h_2 = state_h_2.to(device)
        state_c_2 = state_c_2.to(device)
        
        model.train()
        epoch_acc = []
        epoch_loss = []
        for i,(x, y) in enumerate(batch(seq,n_batch,flags.batch_size,device)):
            optimizer.zero_grad()

            logits, (state_h_1, state_c_1),(state_h_2, state_c_2) = model(x, (state_h_1, state_c_1),(state_h_2, state_c_2))

            #print("shape input {} , shape output {} ".format(np.shape(x),np.shape(logits)))

            #print(np.shape(logits),np.shape(y))
            loss = loss_function(logits, y)

            resp = logits.detach().cpu()

            if e == 90 : 
                stream(x,y,resp)
            acc = accuracy(y,resp)
            epoch_acc.append(acc)
            state_h_1 = state_h_1.detach()
            state_c_1 = state_c_1.detach()
            state_h_2 = state_h_2.detach()
            state_c_2 = state_c_2.detach()

            loss_value = loss.item()
            epoch_loss.append(loss_value)
            loss.backward()
            _ = torch.nn.utils.clip_grad_norm_(model.parameters(), flags.gradients_norm)
            optimizer.step()

        model.eval()
        epoch_acc_test = []
       
        print("epoch : {}  loss {} acc train : {} ".format(e,np.mean(epoch_loss),np.mean(epoch_acc)))
        total_acc.append(np.mean(epoch_acc))
        total_loss.append(np.mean(epoch_loss))

    """for name, param in model.named_parameters():
        if param.requires_grad:
            print(name, param.data)"""

    return model , total_acc  , total_loss , flags.lr

if __name__ == "__main__":
    model , total_acc , total_loss  , lr = train()
    torch.save(model,'save/model')

    def count_parameters(model):
        return sum(p.numel() for p in model.parameters() if p.requires_grad)
    print("nombre paramètre ",count_parameters(model))

    pred(model,"""a matter of fact the european feels this tension as
    a state of distress and twice attempts have been""")
    """fig, axs = plt.subplots(2, 1)

    axs[0].plot(  np.arange(0.0,len(total_acc), 1),total_acc)
    axs[0].set_title('accuracy  trainning du modèle avec {} comme learning rate et {} epochs'.format(lr,len(total_loss)))
    axs[0].set_xlabel('Epochs')
    axs[0].set_ylabel('accuracy min : 0 max : 1')


    axs[1].plot( np.arange(0.0,len(total_loss), 1),total_loss)
    axs[1].set_title('loss du modèle avec {} comme learning rate et {} epochs'.format(lr,len(total_loss)))
    axs[1].set_xlabel('Epochs')
    axs[1].set_ylabel('Loss')

    
    fig.tight_layout(pad=3.0)

    plt.show()"""
