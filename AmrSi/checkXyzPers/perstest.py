# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import sklearn.linear_model as lm  # Machine learning
from sklearn.decomposition import PCA  # for PCA
from sklearn.model_selection import train_test_split

root="/home/okugawa/HDNNP/Si-amr/amr216/pers/"
plotdir=root+"plot/"
smpls=471

pdv=np.load(root+"pdvects.npz")
pdvects= pdv['arr_0']
print(f'Shape of pdvects= {pdvects.shape}')
print(f'Min of pdvects= {pdvects.min()}')
print(f'Max of pdvects= {pdvects.max()}')

#normalize
pdvects = pdvects / pdvects.max()

pca = PCA(n_components=2)
pca.fit(pdvects)
print(f'Shape of PCA comp = {np.array(pca.components_).shape}')
reduced = pca.transform(pdvects)  # すべてのデータを2次元に落とす
out1file=plotdir+'dbg100.txt'
with open(out1file,'w') as out1:
    for redc in reduced:
        if len(redc)!=2:
            print(f'Warning: Len of redc= {len(redc)}')
        txt=str(redc[0])+" "+str(redc[1])+"\n"
        out1.write(txt)
print(f'Shape of reduces = {np.array(reduced).shape}')
print(f'Min of reduced[0]= {reduced[:, 0].min()}')
print(f'Max of reduced[0]= {reduced[:, 0].max()}')
print(f'Min of reduced[1]= {reduced[:, 1].min()}')
print(f'Max of reduced[1]= {reduced[:, 1].max()}')
plt.gca().set_aspect('equal')  # 縦横のアスペクト比を揃える
plt.scatter(reduced[:, 0], reduced[:, 1], c="b", marker='.')  # 2D plot
plt.savefig(plotdir+'dbg200.png')
plt.close()