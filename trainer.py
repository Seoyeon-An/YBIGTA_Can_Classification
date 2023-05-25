import torch
import argparse
import os
import numpy as np
import random
import pickle
import pandas as pd

from PIL import Image
from torchvision.datasets import ImageFolder
from torchvision import transforms
from pytorchcv.model_provider import get_model

_default_train_transform = transforms.Compose(
    [
        transforms.RandomCrop(64, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(
            (0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)
        ),
    ]
)

train_img = ImageFolder(root = './download/',
                        transform = _default_train_transform)

def get_PCA_df(vectors, features, targets, scaler : None):

    # vectors : EigenVectors for the main Real Dataset
    # Features : Last Layer features for the files
    # targets : Targets after passing the Layer
    # Scaler : Standarize if the sclaerworks

    standarized_data= scaler.transform(features)
    new_coordinates = np.matmul(vectors, standarized_data.T)
    new_coordinates = np.vstack((new_coordinates, targets)).T
    df = pd.DataFrame(data = new_coordinates,columns=("1st_principal", "2nd_principal", "label"))
    df.sort_values(by=['label'], axis = 0, inplace = True)
    return df

def seed_everything(seed : int):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True
    
def set_gpu_id(id : int):
    device = torch.device(f"cuda:{id}" if torch.cuda.is_available() else "cpu")
    print(device)
    return device


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Utilize avalianche')
    
    parser.add_argument('--gpu', default = 0, type = int, help = 'Set GPU ID')
    parser.add_argument('--train', default= "./folds/fold/train_dataset.pkl")
    parser.add_argument('--seed', default = 777, type = int, help = 'Set seed to stable reuslt' )
    parser.add_argument('--opt', default = 'Adam', type = str, help = "Set Optimizer")
    parser.add_argument('--lr', default = 0.01, type = float, help = 'Set Learning Rate' )
    parser.add_argument('--epochs', default = 10, type = int, help = 'Set total epoches')
    
    args = parser.parse_args()
    seed_everything(args.seed)
    cur_device = set_gpu_id(args.gpu)
    
    with open(args.train, 'rb') as f:
        train_dataset = pickle.load(f)
    
    
    args = parser.parse_args()
    
    seed_everything(args.seed)
    cur_device = set_gpu_id(args.gpu)
    model = get_model('resnet50')
    model = model.cuda()
    print('Network Ready')
    
    
    
    
