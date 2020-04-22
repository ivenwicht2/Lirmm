import torch
import numpy as np 

model = torch.load("save/model")
vocab_to_int = np.load("save/vocab_to_int.npy",allow_pickle='TRUE').item()
int_to_vocab = np.load("save/int_to_vocab.npy",allow_pickle='TRUE').item()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.eval()

top_k = 5
words = ['i','am']

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

for _ in range(100):
    ix = torch.tensor([[choice]],dtype=torch.int64).to(device)
    output, (state_h_1, state_c_1),(state_h_2, state_c_2) = model(ix, (state_h_1, state_c_1),(state_h_2, state_c_2))

    _, top_ix = torch.topk(output[0], k=top_k)
    choices = top_ix.tolist()
    choice = np.random.choice(choices[0])
    words.append(int_to_vocab[choice])

print(' '.join(words))



