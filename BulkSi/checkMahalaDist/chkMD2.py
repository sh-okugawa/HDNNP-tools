# -*- coding: utf-8 -*-
import sys
import numpy as np
from itertools import islice
import scipy.spatial.distance as SSD
import matplotlib.pyplot as plt
import math

"""
This script is calculating Mahalanobis distance of each predict's PCx
then plot scatter of M-dist mean and TC err 
"""

def plotL2TC(LC7root, outfolder, ph3folder, grps, md):
    colors=["purple","orange","pink","lime","cyan","green","b","red"]
    plotfileT=outfolder+"SFmeanMDtTC3.png"

    SFMDtTC= []
    for grpnum,grp in enumerate(grps):
        clr=colors[grpnum]

        for i in range(1,11):
            datadir=LC7root+grp+"/"+str(i)
            if grp=='mix':
                datadir=datadir+"/1"

            SFdtt=np.empty(0)
            SFt_mean=np.empty(0)
            #Read Symmetry_Function of Train and get Inverse of covariance matrix
            symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
            symt= np.load(symfft, allow_pickle=True)
            symdtt= symt['sym_func']
            lenSFt= len(symdtt[0][0])
            SFdtt= symdtt.reshape(-1,lenSFt)
            SFt_mean= SFdtt.mean(axis=0, keepdims=True)
            SFt_cov= np.cov(SFdtt, rowvar=False)
            invcovSFt=np.linalg.inv(SFt_cov)
            
            #Read Symmetry_Function of TC-predict and get Inverse of covariance matrix 
            symffp=datadir+ph3folder+"/output-phono3py/symmetry_function-pred.npz"
            symp= np.load(symffp, allow_pickle=True)
            symdtp= symp['sym_func']
            lenSFp= len(symdtp[0][0])
            SFdtp= symdtp.reshape(-1,lenSFp)
            if lenSFt!=lenSFp or len(SFt_mean[0])!=lenSFt:
                print(f'Symm_Func length error: SFt={lenSFt} SFp={lenSFp} SFt-mean={len(SFt_mean)}')
                sys.exit()
        
            #Calculate Mahalanobis distance based on PCx of Train symm_func
            MdistT=[]
            for SFp in SFdtp:
                diffSF=SFp-SFt_mean
                diffSFT=diffSF.T
                MD1=np.dot(diffSF,invcovSFt)
                MD=math.sqrt(np.dot(MD1[0],diffSF[0]))
                MdistT.append(MD)
            MDaveT=sum(MdistT)/len(MdistT)

            #Read 300K TC data and get err by subtracting 112.1W/m-K                     
            TCfile =datadir+ph3folder+"/out.txt"
            with open(TCfile, 'r') as TCf:
                for n, line in enumerate(TCf):
                    if 'Thermal conductivity (W/m-k)' in line:
                        TCf.seek(0)
                        for lined in islice(TCf, n+32, n+33):
                            data=lined.split()
                            if data[0]!="300.0":
                                print(f'TC read error: [{data[0]}]K data is read')
                                sys.exit()
                            TCerr=abs(float(data[1])-112.1)
    
            SFMDtTC.append([MDaveT,TCerr,clr])
            
        print(f'[{md}/{grp}:{len(SFMDtTC)}] of M-dist & TC err is gathered')

    #Plot scatter of TC err & Mahalanobis distance based on Train symm_func            
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(f'[{md}] TC err & Mahalanobis dist of Symm_Func (Train base)')
    ax.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax.set_ylabel("Mean of Mahalanobis distance of Symm_Func")
    ax.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for SFMDT in SFMDtTC:
        ax.scatter(SFMDT[1], SFMDT[0], c=SFMDT[2], marker='.')
    left, right = ax.get_xlim()
    ax.set_xlim(-2, right*1.2)
    #ax4 is only for plotting legend of all kind of data
    plt.rcParams["legend.borderpad"] ='0.3'    #Space between handle & edge
    plt.rcParams["legend.handlelength"] ='1'   #Length of handle
    plt.rcParams["legend.handletextpad"] ='0.2' #Space between handle & label
    plt.rcParams["legend.columnspacing"] ='1'  #Space between columns
    plt.rcParams["legend.labelspacing"] ='0.2' #Space between row of label
    ax4 = ax.twinx()
    for i,grp in enumerate(grps):
        lbl="LC="+grp
        clr=colors[i]
        ax4.scatter(SFMDT[1], SFMDT[0],c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax.legend(handler4, label4,loc='lower right',title='LC grp')
    fig.delaxes(ax4)
    plt.savefig(plotfileT)
    plt.close()

if __name__ == '__main__': 
    #calculate Mahalanobis distance of Lammps-MD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/Mdist/chk/"
    ph3folder="/predict-phono3py-3"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,ph3folder,grps,"Lammps-MD-LC7")