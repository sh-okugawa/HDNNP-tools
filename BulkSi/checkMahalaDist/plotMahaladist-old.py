# -*- coding: utf-8 -*-

import sys
import numpy as np
import scipy.spatial.distance as SSD
import matplotlib.pyplot as plt

"""
This script is calculating covariance of train's symm_func
and calculating Mahalanobis distance of each predict's symm_func
  Train_SF:(630[sample]x64[atom]x41[SF]) => reshape (40320x41) => 
  ave:(41) & cov:(41x41) => inv_cov (41x41) => 
  Calculate Mahalanobis dist by [one of predict's SF, ave, inv_cov]
"""

def plotL2TC(LC7root, outfolder, grps, md):
    boxdic={"facecolor" : "lightcyan", "edgecolor" : "navy"}
    
    for grp in grps:
        datadir=LC7root+grp+"/1"
        plotfile=outfolder+grp+"-MDhist.png"
        covfile=outfolder+grp+"-cov.csv"
        if grp=='mix':
            datadir=datadir+"/1"
        
        #Read Symmetry_Function of Train and get Inverse of covariance matrix
        symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
        symt= np.load(symfft)
        symdtt= symt['sym_func']
        lenSFt= len(symdtt[0][0])
        SFdtt= symdtt.reshape(-1,lenSFt)
        SFt_mean= SFdtt.mean(axis=0, keepdims=True)
        SFt_cov= np.cov(SFdtt, rowvar=False)
        invcovSF=np.linalg.pinv(SFt_cov)
        np.savetxt(covfile, SFt_cov, delimiter=',')
        
        #Read Symmetry_Function of TC-predict 
        symffp=datadir+"/predict-phono3py-2/output-phono3py/symmetry_function-pred.npz"
        symp= np.load(symffp)
        symdtp= symp['sym_func']
        lenSFp= len(symdtp[0][0])
        SFdtp= symdtp.reshape(-1,lenSFp)
        if lenSFt!=lenSFp or len(SFt_mean[0])!=lenSFt:
            print(f'Symm_Func length error: SFt={lenSFt} SFp={lenSFp} SFt-mean={len(SFt_mean)}')
            sys.exit()
        
        #Calculate Mahalanobis distance of each predict's symm_func
        Mdist=[]
        for SFp in SFdtp:
            MD=SSD.mahalanobis(SFp,SFt_mean,invcovSF)
            Mdist.append(MD)
        MDave=sum(Mdist)/len(Mdist)
            
        #Plot histgram of diff and report its ave and number of same-G        
        txt1="Total data#= "+str(len(SFdtp))+"\n"
        txt2="   (TC-predict:  "+str(len(symdtp))+")\n"
        txt3="   (Atoms/smpl:  "+str(len(symdtp[0]))+")\n"
        txt4="Train sample#= "+str(len(SFdtt))+"\n\n"
        txt5="Ave of M-dist= "+str(f'{MDave:.02f}')
        L2txt=txt1+txt2+txt3+txt4+txt5

        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.rcParams["legend.edgecolor"] ='green'
        xlbl="Mahalanobis distance"
        ttl="["+md+"/"+grp+"] Mahalanobis distance of Predict symm_func"
        plt.title(ttl)
        ax.set_xlabel(xlbl)
        ax.hist(Mdist,bins=50)
        ax.text(0.98,0.97,L2txt,size=8,ha='right',va='top',
         transform=ax.transAxes,bbox=boxdic,multialignment='left')
        plt.savefig(plotfile)
        print(f'[{md}/{grp}] Mahalanobis distance is plotted')
        plt.close()

if __name__ == '__main__': 
    #calculate the diff of Lammps-MD LC7 Symm_Func of Train & Predict
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/Mdist/"
    rstfile=root+"result-LC7/RMSETCdata.csv"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,grps,"Lammps-MD-LC7")
    
    #calculate the diff of AIMD LC7 Symm_Func of Train & Predict
    root="/home/okugawa/HDNNP/Si-190808-md/"
    LC7root=root+"1000K-LC7n/"
    outfolder=root+"result-LC7n/Mdist/"
    rstfile=root+"result-LC7n/RMSETCdata.csv"
    grps=['0.95','0.97','0.99','1.0','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,grps,"AIMD-LC7")  