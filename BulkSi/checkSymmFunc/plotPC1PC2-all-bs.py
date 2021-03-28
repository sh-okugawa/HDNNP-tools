# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

"""
This script is for plotting PCx data and PC1/PC2 scattering
after PCA and shuffle which is loaded from preprocd_dataset.npz
of all bs samples

preprocd_dataset.npz is saved dataset with following shape
{'dataset':
    [{'inputs/0': array([atoms(=64)x[G-parameters(=41)]]),
      'inputs/1': array([atoms(=64)x[G-parameters(=41)x[diffed(=64x3)]]]),
      'labels/0': array([(=1)]),
      'labels/1': array([[(=192)]])}
     {'inputs/0': ...           }
     ... (number of samples) ...     
     {'inputs/0': ...           } 
    ]
}
"""

def PCplot(dtsetfile, plotdir, grpname):
    dtset= np.load(dtsetfile, allow_pickle=True)
    #allow_pickle op is for adapting spec change of numpy 1.16.3 and later
    dts= dtset['dataset']
    dataset0=[]

    for dt in dts:
        dt0=dt['inputs/0']
        dataset0.append(dt0)

    dim0=len(dataset0)
    dim1=len(dataset0[0])
    dim2=len(dataset0[0][0])
    print(f'{grpname}: Shape of dataset0= {dim0} x {dim1} x {dim2}')

### plot heatmap of one sample of inputs/0
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    xlb=[]
    ylb=[]
    for i in range(1, 42):
        xlb.append("PC"+str(i))
    for i in range(1, 65):
        ylb.append("A"+str(i))

    smpl1=dataset0[0]  ## Pick up sample No.1
    df=pd.DataFrame(data=smpl1, index=ylb, columns=xlb)
    fig, ax1 = plt.subplots(figsize=(12, 9)) 
    sns.heatmap(df, cmap='tab20')
    plottitle1="["+grpname+"] "+"PCx Heatmap of sample#0"
    plt.title(plottitle1)
    plotfile1=plotdir+grpname+"-data1.png"
    plt.savefig(plotfile1)
    plt.close()

### plot scatter of inputs/0 PC1&PC2
    fig = plt.figure()
    ax2 = fig.add_subplot(111)
    plottitle2="["+grpname+"] "+"PC1 & PC2 of inputs/0"
    plt.title(plottitle2)

    ax2.set_xlabel("PC1")
    ax2.set_ylabel("PC2")
    ax2.grid(True)
                
    for dt in dataset0:
        dtt=dt.T
        ax2.scatter(dtt[0],dtt[1],marker='.')
    plotfile2=plotdir+grpname+"-PC1PC2.png"
    plt.savefig(plotfile2)
    plt.close() 

if __name__ == '__main__': 
    root=os.getcwd()
 
    bsxs=["bs1","bs2","bs3","bs4","bs5","bs6","bs7","bs8"]
    plotdir=root+"/result/PCA/"

    for bsx in bsxs:
        for j in range(1,11):
            grpname=bsx+"-"+str(j)
            dtsetdir=root+"/"+bsx+"-d20n50/"+str(j)
            dtsetfile=dtsetdir+"/data/CrystalSi64/preprocd_dataset.npz"
            PCplot(dtsetfile, plotdir, grpname)
            