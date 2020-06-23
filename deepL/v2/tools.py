import numpy as np
import torch 

def stream(x,target,y):
    int_to_vocab = np.load("save/int_to_vocab.npy",allow_pickle='TRUE').item()

    
    x = x.detach().cpu()
    target = target.detach().cpu()

    print("\nx shape : {} , y shape : {} , target shape : {}".format(np.shape(x),np.shape(y),np.shape(target)))
    
    for bash in range(len(y)) :
        print("x : " , end="")
        print(" ".join([int_to_vocab[int(el)] for el in x[bash]]) )
        print("\ny :" , end="")
        print("",int_to_vocab[ int(np.argmax(y[bash]))] ) 
        print("\ntarget :" , end="")
        print("",int_to_vocab[ int(target[bash])] )  


def accuracy(y,target):
    y = y.detach().cpu()

    acc = []

    for bash in range(len(y)) :
        if int(y[bash]) == int(np.argmax(target[bash])) : acc.append(1)
        else : acc.append(0)
    return np.mean(acc)


def pred(model,sentence):
    vocab_to_int = np.load("save/vocab_to_int.npy",allow_pickle='TRUE').item()
    int_to_vocab = np.load("save/int_to_vocab.npy",allow_pickle='TRUE').item()
    model.eval()
    top_k = 5
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    #sentence ="supposing that Truth is a woman what then  Is there not ground for suspecting"
    sentence = sentence.lower()


    words = [ i for i in sentence]
    (state_h_1, state_c_1),(state_h_2, state_c_2) = model.zero_state(1)
    state_h_1 = state_h_1.to(device)
    state_c_1 = state_c_1.to(device)
    state_h_2 = state_h_2.to(device)
    state_c_2 = state_c_2.to(device)

    for w in words:
        ix = torch.tensor([[vocab_to_int[w]]]).to(device)
        output, (state_h_1, state_c_1),(state_h_2, state_c_2) = model(ix, (state_h_1, state_c_1),(state_h_2, state_c_2))
    _, top_ix = torch.topk(output[0], k=top_k)
    choices = top_ix.tolist()
    choice = np.random.choice(choices[0])

    words.append(int_to_vocab[choice])

    for _ in range(50):
        ix = torch.tensor([[choice]],dtype=torch.int64).to(device)
        output, (state_h_1, state_c_1),(state_h_2, state_c_2) = model(ix, (state_h_1, state_c_1),(state_h_2, state_c_2))

        _, top_ix = torch.topk(output[0], k=top_k)
        choices = top_ix.tolist()
        choice = np.random.choice(choices[0])
        words.append(int_to_vocab[choice])

    print(''.join(words))