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

def plotL2TC(LC7root, outfolder, ph3folder, grps, md):
    colors=["purple","orange","pink","lime","cyan","green","b","red"]
    plotfileT=outfolder+"SFmeanMDtTC.png"
    plotfileP=outfolder+"SFmeanMDpTC.png"
    boxdic={"facecolor" : "lightcyan", "edgecolor" : "navy"}

    SFMDtTC, SFMDpTC= [],[]
    for grpnum,grp in enumerate(grps):
        clr=colors[grpnum]
        histfileT= outfolder+grp+"-SFMDThist.png"
        histfileP= outfolder+grp+"-SFMDPhist.png"
        
        for i in range(1,11):
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

            #Plot histgram of Mahalanobis distance and its ave based on PCx of Train symm_func
            if i==1:
                #Plot histgram of M-dist based on Train symm_func
                txt1="Total data#= "+str(len(MdistT))+"\n"
                txt2="   (Predict smpl:  "+str(len(dts0p))+")\n"
                txt3="   (Atoms/smpl:  "+str(len(dts0p[0]))+")\n"
                txt4="Base sample#= "+str(len(MdistP))+"\n\n"
                txt5="Ave of M-dist= "+str(f'{MDaveT:.03f}')
                L2txt=txt1+txt2+txt3+txt4+txt5
                fig = plt.figure()
                ax = fig.add_subplot(111)
                plt.rcParams["legend.edgecolor"] ='green'
                xlbl="Mahalanobis distance of Predict Symm_Func"
                ttl="["+md+"/"+grp+"] Mahalanobis distance (Train Symm_Func base)"
                plt.title(ttl)
                ax.set_xlabel(xlbl)
                ax.hist(MdistT,bins=30)
                ax.text(0.98,0.97,L2txt,size=8,ha='right',va='top',
                 transform=ax.transAxes,bbox=boxdic,multialignment='left')
                plt.savefig(histfileT)
                plt.close()
                
                #Plot histgram of M-dist based on Predict symm_func
                txt1="Total data#= "+str(len(MdistP))+"\n"
                txt2="   (Train smpl:  "+str(len(dts0t))+")\n"
                txt3="   (Atoms/smpl:  "+str(len(dts0t[0]))+")\n"
                txt4="Base sample#= "+str(len(MdistT))+"\n\n"
                txt5="Ave of M-dist= "+str(f'{MDaveP:.03f}')
                L2txt=txt1+txt2+txt3+txt4+txt5
                fig = plt.figure()
                ax = fig.add_subplot(111)
                plt.rcParams["legend.edgecolor"] ='green'
                xlbl="Mahalanobis distance of Train Symm_Func"
                ttl="["+md+"/"+grp+"] Mahalanobis distance (Predict Symm_Func base)"
                plt.title(ttl)
                ax.set_xlabel(xlbl)
                ax.hist(MdistP,bins=30)
                ax.text(0.98,0.97,L2txt,size=8,ha='right',va='top',
                 transform=ax.transAxes,bbox=boxdic,multialignment='left')
                plt.savefig(histfileP)
                plt.close()
                print(f'[{md}/{grp}] Mahalanobis distance of Symm_Func is plotted')

    #Plot scatter of TC err & Mahalanobis distance based on Train symm_func            
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(f'[{md}] TC err & Mahalanobis distance of PCx (Train base)')
    ax.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax.set_ylabel("Mean of Mahalanobis distance of PCx")
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

    #Plot scatter of TC err & Mahalanobis distance based on Predict symm_func            
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(f'[{md}] TC err & Mahalanobis distance of PCx (Predict base)')
    ax.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax.set_ylabel("Mean of Mahalanobis distance of PCx")
    ax.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for SFMDP in SFMDpTC:
        ax.scatter(SFMDP[1], SFMDP[0], c=SFMDP[2], marker='.')
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
    plt.savefig(plotfileP)
    print(f'[Train-B:{len(SFMDtTC)} & Predict-B:{len(SFMDpTC)}] of L2 & TC err is plotted')
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