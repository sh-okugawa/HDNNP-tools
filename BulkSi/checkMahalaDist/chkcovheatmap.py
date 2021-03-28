# -*- coding: utf-8 -*-
import sys
import numpy as np
import scipy.spatial.distance as SSD
import matplotlib.pyplot as plt
#import seaborn as sns
#import pandas as pd

"""
This script is calculating Mahalanobis distance of each predict's Symm_Func
then plot scatter of M-dist mean and TC err 
"""

def plotcovHeatmap(LC7root, outfolder, ph3folder, grps, xlb, md):
    boxdic={"facecolor" : "lightcyan", "edgecolor" : "navy"}

    for grp in grps:
        for i in range(1,11):
            datadir=LC7root+grp+"/"+str(i)
            if grp=='mix':
                datadir=datadir+"/1"
                
#            plotfile=outfolder+grp+"-"+str(i)+"-covHeat.png"
            histfile=outfolder+grp+"-"+str(i)+"-hist.png"
            
            #Read Symmetry_Function of Train and get Inverse of covariance matrix
            symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
            symt= np.load(symfft)
            symdtt= symt['sym_func']
            lenSFt= len(symdtt[0][0])
            SFdtt= symdtt.reshape(-1,lenSFt)
            SFt_mean= SFdtt.mean(axis=0, keepdims=True)
            SFt_cov= np.cov(SFdtt, rowvar=False)
            invcovSFt=np.linalg.pinv(SFt_cov)

            #Read Symmetry_Function of TC-predict and get Inverse of covariance matrix 
            symffp=datadir+ph3folder+"/output-phono3py/symmetry_function-pred.npz"
            symp= np.load(symffp)
            symdtp= symp['sym_func']
            lenSFp= len(symdtp[0][0])
            SFdtp= symdtp.reshape(-1,lenSFp)

            if lenSFt!=lenSFp or len(SFt_mean[0])!=lenSFt:
                print(f'Symm_Func length error: SFt={lenSFt} SFp={lenSFp} SFt-mean={len(SFt_mean)}')
                sys.exit()
        
            #Calculate Mahalanobis distance based on Train symm_func
            MdistT=[]
            for SFp in SFdtp:
                MD=SSD.mahalanobis(SFp,SFt_mean,invcovSFt)
                MdistT.append(MD)
            MDaveT=sum(MdistT)/len(MdistT)

            #Plot histgram of M-dist based on Train symm_func
            txt1="Total data#= "+str(len(SFdtp))+"\n"
            txt2="   (Predict smpl:  "+str(len(symdtp))+")\n"
            txt3="   (Atoms/smpl:  "+str(len(symdtp[0]))+")\n"
            txt4="Base sample#= "+str(len(SFdtt))+"\n\n"
            txt5="Ave of M-dist= "+str(f'{MDaveT:.03f}')
            L2txt=txt1+txt2+txt3+txt4+txt5
            fig = plt.figure()
            ax = fig.add_subplot(111)
            plt.rcParams["legend.edgecolor"] ='green'
            xlbl="Mahalanobis distance of Predict Symm_Func"
            ttl="["+md+"/"+grp+"/"+str(i)+"] SF Mahalanobis dist (Train base)"
            plt.title(ttl)
            ax.set_xlabel(xlbl)
            ax.hist(MdistT,bins=30)
            ax.text(0.98,0.97,L2txt,size=8,ha='right',va='top',
             transform=ax.transAxes,bbox=boxdic,multialignment='left')
            plt.savefig(histfile)
            plt.close()
            
            #Plot Predict Symm_Func
            plotfile=outfolder+grp+"-"+str(i)+"-PSF.png"
            fig = plt.figure(figsize=(8, 4))
            ax1 = fig.add_subplot(111)
            ttl1=f'[{md}/{grp}/{str(i)}] Predict Symm_Func'
            ax1.set_title(ttl1)
            ax1.set_ylabel("Predict Symm_Func")
            ax1.grid(True)
            for SFpp in SFdtp:
                ax1.scatter(xlb, SFpp, marker='.')
            labels = ax1.get_xticklabels()
            plt.setp(labels, rotation=90, fontsize=8);
            plt.savefig(plotfile)
            plt.close()
            
        print(f'{md}/{grp} is plotted')

#            df=pd.DataFrame(data=SFt_cov, index=xlb, columns=xlb)
#            fig, ax = plt.subplots(figsize=(10, 8)) 
#            sns.heatmap(df, cmap='Reds')
#            ttl1=f'[{md}/{grp}] Covariance matrix of Train PCx'
#            ax.set_title(ttl1)
#            txt="Ave of M-dist= "+str(f'{MDaveT:.03f}')
#            ax.text(0.3,0.97,txt,size=10,ha='center',va='top',
#                 transform=ax.transAxes,bbox=boxdic,multialignment='left')
#            plt.savefig(plotfile)
#            plt.close()

if __name__ == '__main__':
    grps=['1.05','mix']
    xlb=["G1"]
    for i in range(1, 25):
        xlb.append("G2-"+str(i))
    for i in range(1, 17):
        xlb.append("G4-"+str(i))
    
    LC7root="/home/okugawa/HDNNP/Si-190808/1000K-LC7/"
#    outfolder="/home/okugawa/HDNNP/Si-190808/result-LC7/Mdist/cov/"
    outfolder="/home/okugawa/HDNNP/Si-190808/result-LC7/Mdist/chk/"
    ph3folder="/predict-phono3py-3"
    plotcovHeatmap(LC7root,outfolder,ph3folder,grps,xlb,"Lammps-MD-LC7")