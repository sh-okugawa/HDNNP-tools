# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

"""
This script is for plotting PCx data of calculated Symm-Func for
train and predict of Lammps-MD 1000K LC7 
"""

def plotG2(symdtt, symdtp, grp, plotfile, xlb, md):
    #Plot PCx data of Train 
    fig = plt.figure(figsize=(14, 4))

    ax1 = fig.add_subplot(1,2,1)
    ttl1=f'[{md}/{grp}] PCx of Train symm_func ({len(symdtt)}x{len(symdtt[0])}x{len(symdtt[0][0])})'
    ax1.set_title(ttl1)
    ax1.set_ylabel("Value of PCx")
    ax1.grid(True)
    for eachsample in symdtt:
        for gdata in eachsample:
            ax1.scatter(xlb, gdata, c='b', marker='.')
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8);
    
    #Plot PCx data of Predict 
    ax2 = fig.add_subplot(1,2,2)
    ttl2=f'[{md}/{grp}] PCx of Predict symm_func ({len(symdtp)}x{len(symdtp[0])}x{len(symdtp[0][0])})'
    ax2.set_title(ttl2)
    ax2.set_ylabel("Value of PCx")
    ax2.grid(True)
    for eachsample in symdtp:
        for gdata in eachsample:
            ax2.scatter(xlb, gdata, c='green', marker='.')
    labels = ax2.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8);
    
    plt.savefig(plotfile)
    print(f'PCx-data of {grp} Train & Predict is plotted')
    plt.close()

def gatherG(root, outfolder, grps, md):
    xlb=[]
    for i in range(1, 42):
        xlb.append("PC"+str(i))

    for grp in grps:
        plotfile=outfolder+grp+"-TP-PCx.png"
        if grp=='mix':
            datadir=root+grp+"/1/1"
        else:
            datadir=root+grp+"/1"

        #Read PCx of Train's Symmetry_Function and get Inverse of covariance matrix
        dtsetfile=datadir+"/data/CrystalSi64/preprocd_dataset.npz"
        dtset= np.load(dtsetfile, allow_pickle=True)
        dts= dtset['dataset']
        dts0t=[]
        for dt in dts:
            dt0t=dt['inputs/0']
            dts0t.append(dt0t)

        #Read PCx of TC-predict's Symmetry_Function  
        pdtsetfile=datadir+"/predict-phono3py-3/output-phono3py/symmetry_function-pred-prepro.npz"
        dtsetp= np.load(pdtsetfile, allow_pickle=True)
        dtsp= dtsetp['dataset']
        dts0p=[]
        for dt in dtsp:
            dt0p=dt['inputs/0']
            dts0p.append(dt0p)

        print(f'PCx of {grp} is gathered')
        plotG2(dts0t, dts0p, grp, plotfile, xlb, md)
        
if __name__ == '__main__': 
    #Plot Lammps-MD LC7 Symm_Func of Train & Predict
    root="/home/okugawa/HDNNP/Si-190808/1000K-LC7/"
    outfolder="/home/okugawa/HDNNP/Si-190808/result-LC7/PCx/"
    grps=['mix','0.95','0.97','0.99','1.00','1.01','1.03','1.05']
    gatherG(root, outfolder, grps, "Lammps-MD")