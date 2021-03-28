# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

"""
This script is calculating Mahalanobis distance of each predict's PCx
then plot scatter of M-dist mean and TC err 
"""

def plotL2TC(LC7root, outfolder, ph3folder, grps, md):
    xlb=['2','3','4','5','6','7','8','9','10']

    for grpnum,grp in enumerate(grps):
        difffile=outfolder+grp+"-PCxdiff.png"

        #Read Symmetry_Function of Train and get Inverse of covariance matrix
        datadir=LC7root+grp+"/1"
        if grp=='mix':
            datadir=datadir+"/1"

        #Read PCx of Train's Symmetry_Function and get Inverse of covariance matrix
        dtsetfile=datadir+"/data/CrystalSi64/preprocd_dataset.npz"
        dtset= np.load(dtsetfile, allow_pickle=True)
        dts= dtset['dataset']
        dts0t=[]
        for dt in dts:
            dt0t=dt['inputs/0']
            dts0t.append(dt0t)

        lenSFt= len(dts0t[0][0])
        SFdtt= np.array(dts0t).reshape(-1,lenSFt)
        SFt_mean1= SFdtt.mean(axis=0, keepdims=True)
        SFt_cov1= np.cov(SFdtt, rowvar=False)
        invcovSFt1=np.linalg.pinv(SFt_cov1)
        
        L2meanL,L2SFtcovL,L2invcovL=[],[],[]
        
        for i in range(2,11):
            datadir=LC7root+grp+"/"+str(i)
            if grp=='mix':
                datadir=datadir+"/1"

            #Read PCx of Train's Symmetry_Function and get Inverse of covariance matrix
            dtsetfile=datadir+"/data/CrystalSi64/preprocd_dataset.npz"
            dtset= np.load(dtsetfile, allow_pickle=True)
            dts= dtset['dataset']
            dts0t=[]
            for dt in dts:
                dt0t=dt['inputs/0']
                dts0t.append(dt0t)
    
            lenSFt= len(dts0t[0][0])
            SFdtt= np.array(dts0t).reshape(-1,lenSFt)
            SFt_mean= SFdtt.mean(axis=0, keepdims=True)
            SFt_cov= np.cov(SFdtt, rowvar=False)
            invcovSFt=np.linalg.pinv(SFt_cov)
          
            SFt_mean_diff=SFt_mean-SFt_mean1
            SFt_cov_diff=SFt_cov-SFt_cov1
            invcovSFt_diff=invcovSFt-invcovSFt1
            
            L2mean=np.linalg.norm(SFt_mean_diff,ord=2)
            L2SFtcov=np.linalg.norm(SFt_cov_diff,ord=2)
            L2invcov=np.linalg.norm(invcovSFt_diff,ord=2)
            
            L2meanL.append(L2mean)
            L2SFtcovL.append(L2SFtcov)
            L2invcovL.append(L2invcov)
           
        fig = plt.figure(figsize=(12, 4))
        ax1 = fig.add_subplot(1,3,1)
        ttl1=f'[{md}/{grp}] SFmean diff ({len(L2meanL)})'
        ax1.set_title(ttl1)
        ax1.grid(True)
        ax1.scatter(xlb, L2meanL, marker='.')
        ax2 = fig.add_subplot(1,3,2)
        ttl2=f'[{md}/{grp}] SFt_cov diff ({len(L2SFtcovL)})'
        ax2.set_title(ttl2)
        ax2.grid(True)
        ax2.scatter(xlb, L2SFtcovL, marker='.')
        ax3 = fig.add_subplot(1,3,3)
        ttl3=f'[{md}/{grp}] invcov diff ({len(L2invcovL)})'
        ax3.set_title(ttl3)
        ax3.grid(True)
        ax3.scatter(xlb, L2invcovL, marker='.')
        plt.savefig(difffile)
        plt.close()
        
        print(f'[{md}/{grp}:{len(SFdtt)}] of SF/PCx diff is plotted')

if __name__ == '__main__': 
    #calculate Mahalanobis distance of Lammps-MD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/Mdist/chk/"
    ph3folder="/predict-phono3py-3"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,ph3folder,grps,"Lammps-MD-LC7")