import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import LabelEncoder
from torch.autograd import Variable
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from languageflow.transformer.word_vector import WordVectorTransformer

USE_CUDA = torch.cuda.is_available()
USE_CUDA = False

FloatTensor = torch.cuda.FloatTensor if USE_CUDA else torch.FloatTensor
LongTensor = torch.cuda.LongTensor if USE_CUDA else torch.LongTensor
ByteTensor = torch.cuda.ByteTensor if USE_CUDA else torch.ByteTensor


class TextCNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, output_size, num_kernel=100,
                 kernel_sizes=[3, 4, 5], dropout=0.5):
        super(TextCNN, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.convs = nn.ModuleList(
            [nn.Conv2d(1, num_kernel, (k, embedding_dim)) for k in
             kernel_sizes])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(len(kernel_sizes) * num_kernel, output_size)

    def init_weights(self, pretrained_word_vectors, is_static=False):
        self.embedding.weight = nn.Parameter(
            torch.from_numpy(pretrained_word_vectors).float())
        if is_static:
            self.embedding.weight.requires_grad = False

    def forward(self, x, is_training=False):
        # (B,1,T,D)
        x = self.embedding(x).unsqueeze(1)
        # [(N,Co,W), ...]*len(Ks)
        x = [F.relu(conv(x)).squeeze(3) for conv in self.convs]
        x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in
             x]  # [(N,Co), ...]*len(Ks)

        concated = torch.cat(x, 1)

        if is_training:
            concated = self.dropout(concated)  # (N,len(Ks)*Co)
        y = self.fc(concated)
        # y = F.softmax(y)
        return y


class CategorizedDataset(Dataset):
    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return len(self.y)

    def __init__(self, X, y):
        self.X = X
        self.y = y


class KimCNNClassifier():
    """ An implementation of the model from Kim2014 paper

    Parameters
    ----------
    batch_size: int
        Number of samples per gradient update
    kernel_sizes: list of int
    num_kernel: int
    embedding_dim: int
        only for CNN-rand
    epoch: int
        Number of epochs to train the model
    lr: float, optional
        Learning rate (default: 1e-3)

    Examples
    --------
    >>> from languageflow.flow import Flow
    >>> flow = Flow()
    >>> flow.data(X, y)
    >>> model = Model(KimCNNClassifier(batch_size=5, epoch=150, embedding_dim=300)
    >>> flow.add_model(model, "KimCNNClassifier"))
    >>> flow.train()
    """

    def __init__(self, batch_size=50, kernel_sizes=[3, 4, 5], num_kernel=100,
                 embedding_dim=50,
                 epoch=50, lr=0.001):
        self.batch_size = batch_size
        self.kernel_sizes = kernel_sizes
        self.num_kernel = num_kernel
        self.embedding_dim = embedding_dim

        self.epoch = epoch
        self.lr = lr

    def fit(self, X, y):
        """Fit KimCNNClassifier according to X, y

        Parameters
        ----------
        X : list of string
            each item is a raw text
        y : list of string
            each item is a label
        """
        ####################
        # Data Loader
        ####################
        word_vector_transformer = WordVectorTransformer(padding='max')
        X = word_vector_transformer.fit_transform(X)
        X = LongTensor(X)
        self.word_vector_transformer = word_vector_transformer

        y_transformer = LabelEncoder()
        y = y_transformer.fit_transform(y)
        y = torch.from_numpy(y)
        self.y_transformer = y_transformer

        dataset = CategorizedDataset(X, y)
        dataloader = DataLoader(dataset,
                                batch_size=self.batch_size,
                                shuffle=True,
                                num_workers=4)

        ####################
        # Model
        ####################
        KERNEL_SIZES = self.kernel_sizes
        NUM_KERNEL = self.num_kernel
        EMBEDDING_DIM = self.embedding_dim

        model = TextCNN(
            vocab_size=word_vector_transformer.get_vocab_size(),
            embedding_dim=EMBEDDING_DIM,
            output_size=len(self.y_transformer.classes_),
            kernel_sizes=KERNEL_SIZES,
            num_kernel=NUM_KERNEL)
        if USE_CUDA:
            model = model.cuda()

        ####################
        # Train
        ####################
        EPOCH = self.epoch
        LR = self.lr

        loss_function = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=LR)

        for epoch in range(EPOCH):
            losses = []
            for i, data in enumerate(dataloader):
                X, y = data
                X, y = Variable(X), Variable(y)

                optimizer.zero_grad()
                model.train()
                output = model(X)

                loss = loss_function(output, y)
                losses.append(loss.data.tolist()[0])
                loss.backward()

                optimizer.step()

                if i % 100 == 0:
                    print("[%d/%d] mean_loss : %0.2f" % (
                        epoch, EPOCH, np.mean(losses)))
                    losses = []
        self.model = model

    def predict(self, X):
        """

        Parameters
        ----------
        X : list of string
            Raw texts

        Returns
        -------
        C : list of string
            List labels
        """
        x = self.word_vector_transformer.transform(X)
        x = Variable(LongTensor(x))
        y = self.model(x)
        y = torch.max(y, 1)[1].data.numpy()
        y = self.y_transformer.inverse_transform(y)
        return y
