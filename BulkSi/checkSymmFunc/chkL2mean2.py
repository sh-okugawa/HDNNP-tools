# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

"""
This script is plotting mean of Train & Predict Symm_Func for each LC7
"""

def plotL2TC(LC7root, outfolder, ph3folder, grps, SFxlb, PCxxlb, md):
    colors=["purple","orange","pink","lime","cyan","green","b","red"]
    SFmean, PCxmean= [[] for i in range(len(grps))], [[] for i in range(len(grps))]
    root="/home/okugawa/HDNNP/Si-190808/phono3py-data/"

    #Read PCx of TC-predict's Symmetry_Function 
    pdtsetfile=root+"output-phono3py/symmetry_function-pred-prepro.npz"
    dtsetp= np.load(pdtsetfile, allow_pickle=True)
    dtsp= dtsetp['dataset']
    dts0p=[]
    for dt in dtsp:
        dt0p=dt['inputs/0']
        dts0p.append(dt0p)
    lenPCxp= len(dts0p[0][0])
    PCxdtp= np.array(dts0p).reshape(-1,lenPCxp)
    PCxpmean= PCxdtp.mean(axis=0, keepdims=True)

    for grpnum,grp in enumerate(grps):
        clr=colors[grpnum]
        
        for i in range(1,11):
            datadir=LC7root+grp+"/"+str(i)
            if grp=='mix':
                datadir=datadir+"/1"
            
            #Read PCx of TC-predict's Symmetry_Function 
            pdtsetfile=datadir+"/data/CrystalSi64/preprocd_dataset.npz"
            dtsetp= np.load(pdtsetfile, allow_pickle=True)
            dtsp= dtsetp['dataset']
            dts0p=[]
            for dt in dtsp:
                dt0p=dt['inputs/0']
                dts0p.append(dt0p)
            lenPCxp= len(dts0p[0][0])
            PCxdtp= np.array(dts0p).reshape(-1,lenPCxp)
            PCx_mean= PCxdtp.mean(axis=0, keepdims=True)
            PCxmean[grpnum].append(PCx_mean)

    #Plot mean of Train PCx for each LC group            
    plotfile2=outfolder+"L2-TC/PCxmeanPred.png"
    fig = plt.figure(figsize=(8, 4))
    ax1 = fig.add_subplot(111)
    ttl1=f'[{md}] Mean of Train PCx ({len(PCxdtp)}) & Predict'
    ax1.set_title(ttl1)
    ax1.set_ylabel("Mean of PCx")
    ax1.grid(True)
    for grpnum,PCxm in enumerate(PCxmean):
        clr=colors[grpnum]
        for PCxmm in PCxm:
            ax1.scatter(PCxxlb, PCxmm, c=clr, marker='.',alpha=0.5)
    ax1.scatter(PCxxlb, PCxpmean, c="black", marker='x',alpha=0.4)
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8);

    #ax4 is only for plotting legend of all kind of data
    plt.rcParams["legend.borderpad"] ='0.3'    #Space between handle & edge
    plt.rcParams["legend.handlelength"] ='1'   #Length of handle
    plt.rcParams["legend.handletextpad"] ='0.2' #Space between handle & label
    plt.rcParams["legend.columnspacing"] ='1'  #Space between columns
    plt.rcParams["legend.labelspacing"] ='0.2' #Space between row of label
    plt.rcParams["legend.edgecolor"] ='green'
    ax4 = ax1.twinx()
    for i,grp in enumerate(grps):
        lbl="LC="+grp
        clr=colors[i]
        ax4.scatter(PCxxlb, PCxmm, c=clr,marker='.',label=lbl)
    ax4.scatter(PCxxlb, PCxmm, c="black", marker='x',label="Predict")
    handler4, label4 = ax4.get_legend_handles_labels()
    ax1.legend(handler4, label4,loc='upper right')
    fig.delaxes(ax4)
    plt.savefig(plotfile2)
    plt.close()

if __name__ == '__main__': 
    SFxlb=["G1"]
    for i in range(1, 25):
        SFxlb.append("G2-"+str(i))
    for i in range(1, 17):
        SFxlb.append("G4-"+str(i))

    PCxxlb=[]
    for i in range(1, 42):
        PCxxlb.append("PC"+str(i))

    #calculate Mahalanobis distance of Lammps-MD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/"
    ph3folder="/predict-phono3py-3"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,ph3folder,grps, SFxlb, PCxxlb,"Lammps-MD-LC7")