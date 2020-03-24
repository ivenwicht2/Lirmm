import torch
import numpy as np 

model = torch.load("save/model2")
word2idx = np.load("save/word2idx.npy",allow_pickle='TRUE').item()
idx2word = np.load("save/idx2word.npy",allow_pickle='TRUE').item()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.eval()
model.reset_hidden()

start  = 'je'
tokenizer =[]
for el in start :
    tokenizer.append(word2idx[el])

for i in range(50):
    text = torch.tensor([tokenizer]).to(device)
    pred = model(text)
    _, top_ix = torch.topk(pred[0], k=5)
    choices = top_ix.tolist()
    tokenizer = np.random.choice(choices[0])
    start += idx2word[tokenizer]
    tokenizer = [tokenizer]

print("\n\n\n")
print(start)