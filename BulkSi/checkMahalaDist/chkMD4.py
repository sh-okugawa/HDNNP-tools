# -*- coding: utf-8 -*-
import sys
import numpy as np

"""
This script is calculating Mahalanobis distance of each predict's PCx
then plot scatter of M-dist mean and TC err 
"""

def plotL2TC(LC7root, outfolder, ph3folder, grps, md):
    datadir=LC7root+"mix/1/1"

    symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
    symt= np.load(symfft, allow_pickle=True)
    symdtt= symt['sym_func']
    lenSFt= len(symdtt[0][0])
    SFdtt0= symdtt.reshape(-1,lenSFt)
    SFt_mean0= SFdtt0.mean(axis=0, keepdims=True)
    SFt_cov0= np.cov(SFdtt0, rowvar=False)
    invcovSFt0=np.linalg.inv(SFt_cov0)

    sumdifftot=0

    for grp in grps:
        for i in range(1,11):
            datadir=LC7root+grp+"/"+str(i)
            if grp=='mix':
                datadir=datadir+"/1"

            #Read Symmetry_Function of Train and get Inverse of covariance matrix
            symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
            symt= np.load(symfft, allow_pickle=True)
            symdtt= symt['sym_func']
            lenSFt= len(symdtt[0][0])
            SFdtt= symdtt.reshape(-1,lenSFt)
            SFt_mean= SFdtt.mean(axis=0, keepdims=True)
            SFt_cov= np.cov(SFdtt, rowvar=False)
            invcovSFt=np.linalg.inv(SFt_cov)

            diffSFp=SFt_mean-SFt_mean0
            sumdiff=np.sum(diffSFp)
            diffcov=SFt_cov-SFt_cov0
            sumdiffcov=np.sum(diffcov)
            diffinv=invcovSFt-invcovSFt0
            sumdiffinv=np.sum(diffinv)
            print(f'grp={grp} i={i}  meandiff={sumdiff}  covdiff={sumdiffcov}    invdiff={sumdiffinv}')
            sumdifftot+=sumdiff
        print(f'{grp} is checked')

    print(f'SFt_cov0= {SFt_cov0}')
    print(f'invcovSFt0= {invcovSFt0}')

    datadir=LC7root+"mix/1/1"
    dtsetfile=datadir+"/data/CrystalSi64/preprocd_dataset.npz"
    dtset= np.load(dtsetfile, allow_pickle=True)
    dts= dtset['dataset']
    dts0t0=[]
    for dt in dts:
        dt0t=dt['inputs/0']
        dts0t0.append(dt0t)

    lenSFt= len(dts0t0[0][0])
    SFdtt0= np.array(dts0t0).reshape(-1,lenSFt)
    SFt_mean0= SFdtt0.mean(axis=0, keepdims=True)
    SFt_cov0= np.cov(SFdtt0, rowvar=False)
    invcovSFt0=np.linalg.pinv(SFt_cov0)

    for grp in grps:
        for i in range(1,11):
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

            diffSFp=SFt_mean-SFt_mean0
            sumdiff=np.sum(diffSFp)
            diffcov=SFt_cov-SFt_cov0
            sumdiffcov=np.sum(diffcov)
            diffinv=invcovSFt-invcovSFt0
            sumdiffinv=np.sum(diffinv)
            print(f'grp={grp} i={i}  meandiff={sumdiff}  covdiff={sumdiffcov}    invdiff={sumdiffinv}')
            sumdifftot+=sumdiff
        print(f'{grp} is checked')

    print(f'PCx_cov0= {SFt_cov0}')
    print(f'invcovPCx0= {invcovSFt0}')

if __name__ == '__main__': 
    #calculate Mahalanobis distance of Lammps-MD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/Mdist/chk/"
    ph3folder="/predict-phono3py-3"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,ph3folder,grps,"Lammps-MD-LC7")