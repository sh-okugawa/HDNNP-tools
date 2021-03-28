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

    for grpnum,grp in enumerate(grps):
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
            print(f'[{grp}-SF] SFdtt={SFdtt.shape} SFdtp={SFdtp.shape} SFt_mean={SFt_mean.shape} invcov={invcovSFt.shape}')
        
            #Calculate Mahalanobis distance based on Train symm_func
            SFp=SFdtp[0]
            diffSF=SFp-SFt_mean
            MD1=np.dot(diffSF,invcovSFt)
            MD=math.sqrt(np.dot(MD1[0],diffSF[0]))
            print(f'[{grp}-SF] diffSF={diffSF.shape} MD1={MD1.shape} MD={MD}')
            print(f'SFp={SFp}\n SFt_mean={SFt_mean}\n diffSF={diffSF}\n invcov={invcovSFt}\n MD1={MD1}')

'''
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
            
            #Read PCx of TC-predict's Symmetry_Function  
            pdtsetfile=datadir+"/predict-phono3py-3/output-phono3py/symmetry_function-pred-prepro.npz"
            dtsetp= np.load(pdtsetfile, allow_pickle=True)
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
            print(f'[{grp}-PCx] SFdtt={SFdtt.shape} SFdtp={SFdtp.shape} SFt_mean={SFt_mean.shape} invcov={invcovSFt.shape}')
            
            #Calculate Mahalanobis distance of each predict's symm_func
            SFp=SFdtp[100]
            diffSF=SFp-SFt_mean
            MD1=np.dot(diffSF,invcovSFt)
            MD=math.sqrt(np.dot(MD1[0],diffSF[0]))
            print(f'[{grp}-PCx] diffSF={diffSF.shape} MD1={MD1.shape} MD={MD}')
            print(f'SFp={SFp}\n SFt_mean={SFt_mean}\n diffSF={diffSF}\n invcov={invcovSFt}\n MD1={MD1}')
'''

if __name__ == '__main__': 
    #calculate Mahalanobis distance of Lammps-MD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/Mdist/chk/"
    ph3folder="/predict-phono3py-3"
    grps=['1.00']
    plotL2TC(LC7root,outfolder,ph3folder,grps,"Lammps-MD-LC7")