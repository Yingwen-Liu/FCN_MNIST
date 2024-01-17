import torch

import torch.nn as nn
import torch.nn.functional as F


class FCN(nn.Module):
    def __init__(self, loss_type, num_classes):
        super(FCN, self).__init__()

        self.loss_type = loss_type
        self.num_classes = num_classes

        # 3 fully connected layers
        self.fc1 = nn.Linear(784, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, num_classes)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = torch.tanh(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return F.softmax(x,dim=1)
    
    def get_loss(self, output, target):
        if self.loss_type == 'ce':
            # compute Cross Entropy Loss. No need to one hot the target
            loss = F.cross_entropy(output, target)
        elif self.loss_type == 'l2':
            # compute L2 loss
            target = F.one_hot(target, self.num_classes).float()
            loss = F.mse_loss(output, target)

        return loss

