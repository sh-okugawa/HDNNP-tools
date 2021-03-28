# -*- coding: utf-8 -*-
import sys
import numpy as np
from itertools import islice
import scipy.spatial.distance as SSD
from sklearn import linear_model
import matplotlib.pyplot as plt

"""
This script is calculating Mahalanobis distance of each predict's PCx
then plot scatter of M-dist mean and TC err with coef/R^2/corr data
"""

def plotL2TC(LC7root, outfolder, ph3folder, grps, md):
    colors=["purple","orange","pink","lime","cyan","green","b","red"]
    plotfileT=outfolder+"PCxMDtTC-coef.png"
    plotfileP=outfolder+"PCxMDpTC-coef.png"
    boxdic={"facecolor" : "lightcyan", "edgecolor" : "navy"}
    clf = linear_model.LinearRegression()

    SFMDtTC,SFMDpTC,SFMDtTCcoef,SFMDpTCcoef= [],[],[],[]
    SFMDTCerr,SFMDTCerrL= [],[]
    for grpnum,grp in enumerate(grps):
        clr=colors[grpnum]
        
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
        
            #Read PCx of TC-predict's Symmetry_Function and get Inverse of covariance matrix 
            pdtsetfile=datadir+ph3folder+"/output-phono3py/symmetry_function-pred-prepro.npz"
            dtsetp= np.load(pdtsetfile, allow_pickle=True)
            #allow_pickle op is for adapting spec change of numpy 1.16.3 and later
            dtsp= dtsetp['dataset']
            dts0p=[]
            for dt in dtsp:
                dt0p=dt['inputs/0']
                dts0p.append(dt0p)
    
            lenSFp= len(dts0p[0][0])
            SFdtp= np.array(dts0p).reshape(-1,lenSFp)
            SFp_mean= SFdtp.mean(axis=0, keepdims=True)
            SFp_cov= np.cov(SFdtp, rowvar=False)
            invcovSFp=np.linalg.pinv(SFp_cov)
            
            if lenSFt!=lenSFp or len(SFt_mean[0])!=lenSFt:
                print(f'PCx length error: SFt={lenSFt} SFp={lenSFp} SFt-mean={len(SFt_mean)}')
                sys.exit()
            
            #Calculate Mahalanobis distance based on PCx of Train symm_func
            MdistT=[]
            for SFp in SFdtp:
                MD=SSD.mahalanobis(SFp,SFt_mean,invcovSFt)
                MdistT.append(MD)
            MDaveT=sum(MdistT)/len(MdistT)

            #Calculate Mahalanobis distance based on PCx of Train symm_func
            MdistP=[]
            for SFt in SFdtt:
                MD=SSD.mahalanobis(SFt,SFp_mean,invcovSFp)
                MdistP.append(MD)
            MDaveP=sum(MdistP)/len(MdistP)
            
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
            SFMDpTC.append([MDaveP,TCerr,clr])
            SFMDtTCcoef.append(MDaveT)
            SFMDpTCcoef.append(MDaveP)
            SFMDTCerr.append(TCerr)
            SFMDTCerrL.append([TCerr])

    #Calculate coef, R^2 and corr of each sample for Train-base
    clf.fit(SFMDTCerrL,SFMDtTCcoef)
    coefSFMDtTC= clf.coef_[0]
    R2SFMDtTC= clf.score(SFMDTCerrL,SFMDtTCcoef)
    corrSFMDtTC= np.corrcoef(SFMDTCerr,SFMDtTCcoef)[0][1]

    #Plot scatter of TC err & Mahalanobis distance based on Train symm_func            
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    plt.title(f'[{md}] TC err & Mahalanobis dist of PCx (Train base)')
    ax.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax.set_ylabel("Mean of Mahalanobis distance of PCx")
    ax.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for SFMDT in SFMDtTC:
        ax.scatter(SFMDT[1], SFMDT[0], c=SFMDT[2], marker='.')
    plt.plot(SFMDTCerr, clf.predict(SFMDTCerrL))
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
    
    #Plot text box of coef, R^2, corr info
    txt1="Corr= "+str(f'{corrSFMDtTC:.03f}')+"\n"
    txt2="Coef= "+str(f'{coefSFMDtTC:.03f}')+"\n"
    txt3="R^2=  "+str(f'{R2SFMDtTC:.03f}')
    coeftxt=txt1+txt2+txt3
    ax.text(0.98,0.97,coeftxt,size=10,ha='right',va='top',
     transform=ax.transAxes,bbox=boxdic,multialignment='left')
    plt.savefig(plotfileT)
    plt.close()

    #Calculate coef, R^2 and corr of each sample for Predict-base
    clf.fit(SFMDTCerrL,SFMDpTCcoef)
    coefSFMDpTC= clf.coef_[0]
    R2SFMDpTC= clf.score(SFMDTCerrL,SFMDpTCcoef)
    corrSFMDpTC= np.corrcoef(SFMDTCerr,SFMDpTCcoef)[0][1]

    #Plot scatter of TC err & Mahalanobis distance based on Predict symm_func            
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    plt.title(f'[{md}] TC err & Mahalanobis dist of PCx (Predict base)')
    ax.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax.set_ylabel("Mean of Mahalanobis distance of PCx")
    ax.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for SFMDP in SFMDpTC:
        ax.scatter(SFMDP[1], SFMDP[0], c=SFMDP[2], marker='.')
    plt.plot(SFMDTCerr, clf.predict(SFMDTCerrL))
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
        ax4.scatter(SFMDP[1], SFMDP[0],c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax.legend(handler4, label4,loc='lower right',title='LC grp')
    fig.delaxes(ax4)

    #Plot text box of coef, R^2, corr info
    txt1="Corr= "+str(f'{corrSFMDpTC:.03f}')+"\n"
    txt2="Coef= "+str(f'{coefSFMDpTC:.03f}')+"\n"
    txt3="R^2=  "+str(f'{R2SFMDpTC:.03f}')
    coeftxt=txt1+txt2+txt3
    ax.text(0.98,0.97,coeftxt,size=10,ha='right',va='top',
     transform=ax.transAxes,bbox=boxdic,multialignment='left')
    plt.savefig(plotfileP)
    print(f'[Train-B:{len(SFMDtTC)} & Predict-B:{len(SFMDpTC)}] of M-dist & TC err is plotted')
    plt.close()

if __name__ == '__main__': 
    #calculate Mahalanobis distance of Lammps-MD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/PCx/Mdist/"
    ph3folder="/predict-phono3py-3"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,ph3folder,grps,"Lammps-MD-LC7")
    
    #calculate Mahalanobis distance of AIMD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808-md/"
    LC7root=root+"1000K-LC7n/"
    outfolder=root+"result-LC7n/PCx/Mdist/"
    ph3folder="/predict-phono3py"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,ph3folder,grps,"AIMD-LC7")