import torch

model = torch.load("save/model1")

start  = 'je'

for i in range(500):
    pred = model()