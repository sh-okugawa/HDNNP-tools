# -*- coding: utf-8 -*-
import sys
import numpy as np
import matplotlib.pyplot as plt

"""
This script is plotting the force-difference (L1 norm & L2 norm)
of DFT and HDNNP (predict_phono3py/FORCES_FC3) 
"""

def readFORCES(FRCfile):
    #Making list of FORCES_FC3
    # Returned list format: [[x1,y1,z1], ... ,[xn,yn,zn]]
    datanum=64
    with open(FRCfile,'r') as f1:
        FRCl, frc = [],[]
        frclines = f1.readlines()
        for frcline in frclines:
            row=frcline.split()
            if row[0]=="#":
                if row[1]=="File:":
                    if len(frc)==datanum:
                        FRCl.append(frc)
                        frc=[]
                    elif len(frc)!=0:
                        print(f'Error: {frc[0]} of {FRCfile} has len={len(frc)} data')
                        sys.exit()
            else:
                frc.append([float(row[0])*1000,float(row[1])*1000,float(row[2])*1000])
        if len(frc)==datanum:
            FRCl.append(frc)
        else:
            print(f'Error: {frc[0]} of {FRCfile} has len={len(frc)-1} data')
            sys.exit()
    return(FRCl)

def diffFORCE(DTFl,MDFl):
    #Calculate diff of DFT-force & HDNNP-force
    if len(DTFl)!=len(MDFl):
        print(f"Error: FORCES_FC3 length of DFT={len(DTFl)} & HDNNP={len(MDFl)}")
        sys.exit()

    diffall1, diffall2=[],[]
    difftot1, difftot2=[],[]
    diff=np.array(DTFl)-np.array(MDFl)
    for frc in diff:
        diff1, diff2=[],[]
        for f in frc:
            diff1.append(np.linalg.norm(f,ord=1)) #L1 norm = sum of abs
            diff2.append(np.linalg.norm(f,ord=2)) #L2 norm = sqrt of sum of squares
        diffall1.append(diff1)
        diffall2.append(diff2)
        difftot1.extend(diff1)
        difftot2.extend(diff2)
    
    return([diffall1,diffall2,difftot1,difftot2])
   
def plotDiffFORCE(LC7root,outfolder,DTFl,grps,md):
    #Set X-axis label
    boxdic={"facecolor" : "lightcyan", "edgecolor" : "navy"}
    L1txt="L1-diff<L1 Norm>: [abs(Xdft-Xhdn)+abs(Ydft-Yhdn)+abs(Zdft-Zhdn)]"
    L2txt="L2-diff<L2 Norm>: [SQRT((Xdft-Xhdn)^2+(Ydft-Yhdn)^2+(Zdft-Zhdn)^2)]"
    widths = [6, 1]  #Width ratio of 2 sub-plots

    xlb=[]
    for i in range(len(DTFl)):
        xlb.append(str(i+1))

    for grp in grps:
        diffall1, diffall2=[],[]
        difftot1, difftot2=[],[]
        LC7dir=LC7root+grp+"/"
        plotfile1=outfolder+grp+"-Fdiff(L1).png"
        plotfile2=outfolder+grp+"-Fdiff(L2).png"
        
        #Gather diff of force    
        for i in range(1, 11):
            if grp=='mix':
                FRCfile=LC7dir+str(i)+"/1/predict-phono3py/FORCES_FC3"
            else:
                FRCfile=LC7dir+str(i)+"/predict-phono3py/FORCES_FC3"
            MDFl=readFORCES(FRCfile)
            Diffl=diffFORCE(DTFl, MDFl)
            diffall1.append(Diffl[0])
            diffall2.append(Diffl[1])
            difftot1.extend(Diffl[2])
            difftot2.extend(Diffl[3])

        #Plot diff of force (L1 norm) and histgram of each diff value
        fig = plt.figure(figsize=(14, 4),constrained_layout=True)
        spec = fig.add_gridspec(ncols=2, nrows=1, width_ratios=widths)
        ax1 = fig.add_subplot(spec[0,0])
        ttl=f'[{md}/{grp}] L1-diff of FORCES_FC3 between DFT and HDNNP(64posx10data)'
        plt.title(ttl)
        ax1.set_xlabel("File#")
        ax1.set_ylabel("force diff (meV/A)")
        ax1.text(0.98,0.96,L1txt,size=8,ha='right',va='top',
                 transform=ax1.transAxes,bbox=boxdic)
        ax1.grid(True)
        for diffa1 in diffall1:
            diffa1T=np.array(diffa1).T
            for diffm in diffa1T:
                ax1.scatter(xlb,diffm,c="green",marker='.')
        labels = ax1.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=6);
        ymin, ymax = ax1.get_ylim()
        
        ax2 = fig.add_subplot(spec[0,1])
        ax2.set_ylim(ymin, ymax)
        plt.title("# of diff value")
        ax2.hist(difftot1,bins=30,orientation="horizontal")
        plt.savefig(plotfile1)
        plt.close()
        
        #Plot diff of force (L2 norm) and histgram of each diff value
        fig = plt.figure(figsize=(14, 4),constrained_layout=True)
        spec = fig.add_gridspec(ncols=2, nrows=1, width_ratios=widths)
        ax1 = fig.add_subplot(spec[0,0])
        ttl=f'[{md}/{grp}] L2-diff of FORCES_FC3 between DFT and HDNNP(64posx10data)'
        plt.title(ttl)
        ax1.set_xlabel("File#")
        ax1.set_ylabel("force diff (meV/A)")
        ax1.text(0.98,0.96,L2txt,size=8,ha='right',va='top',
         transform=ax1.transAxes,bbox=boxdic)
        ax1.grid(True)
        for diffa2 in diffall2:
            diffa2T=np.array(diffa2).T
            for diffm in diffa2T:
                ax1.scatter(xlb,diffm,c="blue",marker='.')
        labels = ax1.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=6);
        ymin, ymax = ax1.get_ylim()

        ax2 = fig.add_subplot(spec[0,1])
        ax2.set_ylim(ymin, ymax)
        plt.title("# of diff value")
        ax2.hist(difftot2,bins=30,orientation="horizontal")
        plt.savefig(plotfile2)
        plt.close()
        print(f'Force diff(L1&L2) of {md}/{grp} is plotted')
        
if __name__ == '__main__': 
    #Read FORCES_FC3 of DFT
    DFTforce="/home/okugawa/HDNNP/Si-190808/FORCES/DFT/FORCES_FC3"
    DTFl=readFORCES(DFTforce)
    
    #Read FORCES_FC3 of each and calculate the diff with DFT's
    #Plot Lammps-MD LC7 Symm_Func of Train & Predict
    LC7root="/home/okugawa/HDNNP/Si-190808/1000K-LC7/"
    outfolder="/home/okugawa/HDNNP/Si-190808/result-LC7/TCforce/"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotDiffFORCE(LC7root,outfolder,DTFl,grps,"Lammps-MD-LC7")
    
    #Plot AIMD LC7 Symm_Func of Train & Predict
    LC7root="/home/okugawa/HDNNP/Si-190808-md/1000K-LC7n/"
    outfolder="/home/okugawa/HDNNP/Si-190808-md/result-LC7n/TCforce/"
    grps=['0.95','0.97','0.99','1.0','1.01','1.03','1.05','mix']
    plotDiffFORCE(LC7root,outfolder,DTFl,grps,"AIMD-LC7")   