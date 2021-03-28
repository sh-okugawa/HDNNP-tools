# -*- coding: utf-8 -*-

import sys
import numpy as np
import scipy.spatial.distance as SSD
import matplotlib.pyplot as plt

"""
This script is calculating covariance of train's PCx of symm_func
and calculating Mahalanobis distance of each predict's PC1&PC2&PC3
  PCx of Train_SF:(630[sample]x64[atom]x41[PCx]) => reshape (40320x41) => 
  slice out only PC1&PC2&PC3 a[:, 0:3] => ave:(3) & cov:(3x3) => inv_cov (3x3) => 
  Calculate Mahalanobis dist by [one of predict's PC123, ave, inv_cov]
"""

def plotL2TC(LC7root, outfolder, grps, md):
    boxdic={"facecolor" : "lightcyan", "edgecolor" : "navy"}
    
    for grp in grps:
        datadir=LC7root+grp+"/1"
        plotfile=outfolder+grp+"-PC123-MDhist.png"
        cov123file=outfolder+"cov/"+grp+"-PC123-cov.csv"
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
        SFdtt123= SFdtt[:, 0:3]  #Slice out only PC1&PC2&PC3
        SFt_mean= SFdtt123.mean(axis=0, keepdims=True)
        SFt_cov= np.cov(SFdtt123, rowvar=False)
        invcovSF=np.linalg.pinv(SFt_cov)
        np.savetxt(cov123file, SFt_cov, delimiter=',')
        
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
        SFdtp123= SFdtp[:, 0:3]  #Slice out only PC1&PC2&PC3
        if lenSFt!=lenSFp:
            print(f'PCx length error: SFt={lenSFt} SFp={lenSFp} SFt-mean={len(SFt_mean)}')
            sys.exit()
        
        #Calculate Mahalanobis distance of each predict's symm_func
        Mdist123=[]
        for SFp in SFdtp123:
            MD=SSD.mahalanobis(SFp,SFt_mean,invcovSF)
            Mdist123.append(MD)
        MDave123=sum(Mdist123)/len(Mdist123)
            
        #Plot histgram of diff and report its ave and number of same-G        
        txt1="Total data#= "+str(len(SFdtp))+"\n"
        txt2="   (TC-predict:  "+str(len(dts0p))+")\n"
        txt3="   (Atoms/smpl:  "+str(len(dts0p[0]))+")\n"
        txt4="Train sample#= "+str(len(SFdtt123))+"\n\n"
        txt5="Ave of M-dist= "+str(f'{MDave123:.02f}')
        L2txt=txt1+txt2+txt3+txt4+txt5

        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.rcParams["legend.edgecolor"] ='green'
        xlbl="Mahalanobis distance of PC1&PC2&PC3"
        ttl="["+md+"/"+grp+"] Mahalanobis distance of PC1&PC2&PC3"
        plt.title(ttl)
        ax.set_xlabel(xlbl)
        ax.hist(Mdist123,bins=50)
        ax.text(0.98,0.97,L2txt,size=8,ha='right',va='top',
         transform=ax.transAxes,bbox=boxdic,multialignment='left')
        plt.savefig(plotfile)
        print(f'[{md}/{grp}] Mahalanobis distance of PC123 is plotted')
        plt.close()

if __name__ == '__main__': 
    #calculate the diff of Lammps-MD LC7 Symm_Func of Train & Predict
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/Mdist/"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,grps,"Lammps-MD-LC7")