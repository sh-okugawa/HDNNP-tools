# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

"""
This script is plotting mean of Train Symm_Func/PCx for each LC7
"""

def plotL2TC(LC7root, outfolder, ph3folder, grps, SFxlb, PCxxlb, md):
    colors=["purple","orange","pink","lime","cyan","green","b","red"]
    SFmean,PCxmean= [[] for i in range(len(grps))],[[] for i in range(len(grps))]

    for grpnum,grp in enumerate(grps):
        clr=colors[grpnum]
        
        for i in range(1,11):
            datadir=LC7root+grp+"/"+str(i)
            if grp=='mix':
                datadir=datadir+"/1"
            
            #Read Symmetry_Function of Train
            symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
            symt= np.load(symfft)
            symdtt= symt['sym_func']
            lenSFt= len(symdtt[0][0])
            SFdtt= np.array(symdtt).reshape(-1,lenSFt)
            SF_mean= SFdtt.mean(axis=0, keepdims=True)
            SFmean[grpnum].append(SF_mean)

            #Read PCx of Train's Symmetry_Function
            dtsetfile=datadir+"/data/CrystalSi64/preprocd_dataset.npz"
            dtset= np.load(dtsetfile, allow_pickle=True)
            #allow_pickle op is for adapting spec change of numpy 1.16.3 and later
            dts= dtset['dataset']
            dts0t=[]
            for dt in dts:
                dt0t=dt['inputs/0']
                dts0t.append(dt0t)

            lenPCx= len(dts0t[0][0])
            PCxdtt= np.array(dts0t).reshape(-1,lenPCx)
            PCx_mean= PCxdtt.mean(axis=0, keepdims=True)
            PCxmean[grpnum].append(PCx_mean)

    #Plot mean of Train Symm_Func for each LC group            
    plotfile1=outfolder+"L2-TC/SFmean.png"
    fig = plt.figure(figsize=(8, 4))
    ax1 = fig.add_subplot(111)
    ttl1=f'[{md}] Mean of Train Symm_Func ({len(PCxdtt)})'
    ax1.set_title(ttl1)
    ax1.set_ylabel("Mean of Symm_Func")
    ax1.grid(True)
    for grpnum,SFm in enumerate(SFmean):
        clr=colors[grpnum]
        for SFmm in SFm:
            ax1.scatter(SFxlb, SFmm, c=clr, marker='.')
        labels = ax1.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=8);
    left, right = ax1.get_xlim()
    ax1.set_xlim(-2, right*1.2)
    #ax4 is only for plotting legend of all kind of data
    plt.rcParams["legend.borderpad"] ='0.3'    #Space between handle & edge
    plt.rcParams["legend.handlelength"] ='1'   #Length of handle
    plt.rcParams["legend.handletextpad"] ='0.2' #Space between handle & label
    plt.rcParams["legend.columnspacing"] ='1'  #Space between columns
    plt.rcParams["legend.labelspacing"] ='0.2' #Space between row of label
    ax4 = ax1.twinx()
    for i,grp in enumerate(grps):
        lbl="LC="+grp
        clr=colors[i]
        ax4.scatter(SFxlb, SFmm, c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax1.legend(handler4, label4,loc='lower right',title='LC grp')
    fig.delaxes(ax4)
    plt.savefig(plotfile1)
    plt.close()

    #Plot mean of Train PCx for each LC group            
    plotfile2=outfolder+"L2-TC/PCxmean.png"
    fig = plt.figure(figsize=(8, 4))
    ax2 = fig.add_subplot(111)
    ttl2=f'[{md}] Mean of Train PCx ({len(SFdtt)})'
    ax2.set_title(ttl2)
    ax2.set_ylabel("Mean of Symm_Func")
    ax2.grid(True)
    for grpnum,PCxm in enumerate(PCxmean):
        clr=colors[grpnum]
        for PCxmm in PCxm:
            ax2.scatter(PCxxlb, PCxmm, c=clr, marker='.')
        labels = ax2.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=8);
    left, right = ax2.get_xlim()
    ax2.set_xlim(-2, right*1.2)
    #ax4 is only for plotting legend of all kind of data
    plt.rcParams["legend.borderpad"] ='0.3'    #Space between handle & edge
    plt.rcParams["legend.handlelength"] ='1'   #Length of handle
    plt.rcParams["legend.handletextpad"] ='0.2' #Space between handle & label
    plt.rcParams["legend.columnspacing"] ='1'  #Space between columns
    plt.rcParams["legend.labelspacing"] ='0.2' #Space between row of label
    ax4 = ax2.twinx()
    for i,grp in enumerate(grps):
        lbl="LC="+grp
        clr=colors[i]
        ax4.scatter(PCxxlb, PCxmm, c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax1.legend(handler4, label4,loc='lower right',title='LC grp')
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
    
    #calculate Mahalanobis distance of AIMD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808-md/"
    LC7root=root+"1000K-LC7n/"
    outfolder=root+"result-LC7n/"
    ph3folder="/predict-phono3py"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,ph3folder,grps, SFxlb, PCxxlb,"AIMD-LC7")