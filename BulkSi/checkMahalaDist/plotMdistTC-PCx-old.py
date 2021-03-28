# -*- coding: utf-8 -*-
import sys
import numpy as np
from itertools import islice
import scipy.spatial.distance as SSD
import matplotlib.pyplot as plt

"""
This script is calculating Mahalanobis distance of each predict's PCx
then plot scatter of M-dist mean and TC err 
"""

def plotL2TC(LC7root, outfolder, grps, md):
    colors=["purple","orange","pink","lime","cyan","green","b","red"]
    plotfile=outfolder+"TCe&MD-PCx.png"

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for grpnum,grp in enumerate(grps):
        clr=colors[grpnum]
        for i in range(1,10):
            datadir=LC7root+grp+"/"+str(i)
            if grp=='mix':
                datadir=datadir+"/1"
            
            #Read PCx of Train's Symmetry_Function and get Inverse of covariance matrix
            dtsetfile=datadir+"/data/CrystalSi64/preprocd_dataset.npz"
            dtset= np.load(dtsetfile, allow_pickle=True)
            #allow_pickle op is for adapting spec change of numpy 1.16.3 and later
            dts= dtset['dataset']
            dts0t=[]
            for dt in dts:
                dt0t=dt['inputs/0']
                dts0t.append(dt0t)
    
            lenSFt= len(dts0t[0][0])
            SFdtt= np.array(dts0t).reshape(-1,lenSFt)
            SFt_mean= SFdtt.mean(axis=0, keepdims=True)
            SFt_cov= np.cov(SFdtt, rowvar=False)
            invcovSF=np.linalg.pinv(SFt_cov)
        
            #Read PCx of TC-predict's Symmetry_Function  
            pdtsetfile=datadir+"/predict-phono3py-3/output-phono3py/symmetry_function-pred-prepro.npz"
            dtsetp= np.load(pdtsetfile, allow_pickle=True)
            #allow_pickle op is for adapting spec change of numpy 1.16.3 and later
            dtsp= dtsetp['dataset']
            dts0p=[]
            for dt in dtsp:
                dt0p=dt['inputs/0']
                dts0p.append(dt0p)
    
            lenSFp= len(dts0p[0][0])
            SFdtp= np.array(dts0p).reshape(-1,lenSFp)
            if lenSFt!=lenSFp or len(SFt_mean[0])!=lenSFt:
                print(f'PCx length error: SFt={lenSFt} SFp={lenSFp} SFt-mean={len(SFt_mean)}')
                sys.exit()
            
            #Calculate Mahalanobis distance of each predict's symm_func
            Mdist=[]
            for SFp in SFdtp:
                MD=SSD.mahalanobis(SFp,SFt_mean,invcovSF)
                Mdist.append(MD)
            MDave=sum(Mdist)/len(Mdist)

            #Read 300K TC data and get err by subtracting 112.1W/m-K                     
            TCfile =datadir+"/predict-phono3py-3/out.txt"
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
    
            #Plot scatter of TC err & ave of Mahalanobis distance
            ax.scatter(TCerr,MDave,c=clr,marker='.')

        print(f'[{md}/{grp}] TC err & Ave of Mahalanobis distance of PCx is plotted')
        
    plt.title(f'[{md}] TC err & Mean of Mahalanobis distance of PCx')
    ax.set_xlabel(f'TC Err (fm 112.1W/m-K:300K)')
    ax.set_ylabel(f'Mean of Mahalanobis dist ({lenSFp} PCx)')
    ax.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
  
    left, right = ax.get_xlim()
    ax.set_xlim(-1, right*1.2)
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
        ax4.scatter(TCerr,MDave,c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax.legend(handler4, label4,loc='lower right',title='LC grp')
    fig.delaxes(ax4)
    plt.savefig(plotfile)
    plt.close()

if __name__ == '__main__': 
    #calculate Mahalanobis distance of Lammps-MD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/Mdist/cov/"
    rstfile=root+"result-LC7/RMSETCdata.csv"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,grps,"Lammps-MD-LC7")
    