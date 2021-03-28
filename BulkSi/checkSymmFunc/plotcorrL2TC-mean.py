# -*- coding: utf-8 -*-
import sys
from itertools import islice
import numpy as np
import matplotlib.pyplot as plt

"""
This script is calculating the Euclid distance (L2 norm) 
between Mean of Train symm_func and Predict symm_func,
then plot scatter of L2 norm mean and TC err 
"""

def plotL2TC(LC7root, outfolder, ph3folder, grps, md):
    colors=["purple","orange","pink","lime","cyan","deepskyblue","b","red"]
    plotfileT=outfolder+"SFmeanL2T&TC.png"
    plotfileP=outfolder+"SFmeanL2P&TC.png"
    boxdic={"facecolor" : "lightcyan", "edgecolor" : "navy"}
    
    SFL2TTC, SFL2PTC= [],[]
    for grpnum,grp in enumerate(grps):
        clr=colors[grpnum]
        histfileT= outfolder+grp+"-SFL2Thist.png"
        histfileP= outfolder+grp+"-SFL2Phist.png"
        for i in range(1,11):
            datadir=LC7root+grp+"/"+str(i)
            if grp=='mix':
                datadir=datadir+"/1"
            
            #Calculate L2 norm of Symmetry_Func diff
            symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
            symt= np.load(symfft)
            symdtt= symt['sym_func']
            symffp=datadir+ph3folder+"/output-phono3py/symmetry_function-pred.npz"
            symp= np.load(symffp)
            symdtp= symp['sym_func']
            SFL2=diffSymF(symdtt, symdtp)
            aveL2T=sum(SFL2[0])/len(SFL2[0])
            aveL2P=sum(SFL2[1])/len(SFL2[1])
    
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
    
            SFL2TTC.append([aveL2T, TCerr, clr])
            SFL2PTC.append([aveL2P, TCerr, clr])
            
            #Plot histgram of diff and its ave
            if i==1:
                #Plot histgram of L2 norm based on Train symm_func
                txt1="Total data#= "+str(len(SFL2[0]))+"\n"
                txt2="   (Predict smpl:  "+str(len(symdtp))+")\n"
                txt3="   (Atoms/smpl:  "+str(len(symdtp[0]))+")\n"
                txt4="Base sample#= "+str(len(SFL2[1]))+"\n\n"
                txt5="Ave of L2 norm= "+str(f'{aveL2T:.03f}')
                L2txt=txt1+txt2+txt3+txt4+txt5
                fig = plt.figure()
                ax = fig.add_subplot(111)
                plt.rcParams["legend.edgecolor"] ='green'
                xlbl="Euclid distance of Predict Symm_Func"
                ttl="["+md+"/"+grp+"] Euclid distance (Train Symm_Func base)"
                plt.title(ttl)
                ax.set_xlabel(xlbl)
                ax.hist(SFL2[0],bins=30)
                ax.text(0.98,0.97,L2txt,size=8,ha='right',va='top',
                 transform=ax.transAxes,bbox=boxdic,multialignment='left')
                plt.savefig(histfileT)
                plt.close()
                
                #Plot histgram of L2 norm based on Predict symm_func
                txt1="Total data#= "+str(len(SFL2[1]))+"\n"
                txt2="   (Train smpl:  "+str(len(symdtt))+")\n"
                txt3="   (Atoms/smpl:  "+str(len(symdtt[0]))+")\n"
                txt4="Base sample#= "+str(len(SFL2[0]))+"\n\n"
                txt5="Ave of L2 norm= "+str(f'{aveL2P:.03f}')
                L2txt=txt1+txt2+txt3+txt4+txt5
                fig = plt.figure()
                ax = fig.add_subplot(111)
                plt.rcParams["legend.edgecolor"] ='green'
                xlbl="Euclid distance of Train Symm_Func"
                ttl="["+md+"/"+grp+"] Euclid distance (Predict Symm_Func base)"
                plt.title(ttl)
                ax.set_xlabel(xlbl)
                ax.hist(SFL2[1],bins=30)
                ax.text(0.98,0.97,L2txt,size=8,ha='right',va='top',
                 transform=ax.transAxes,bbox=boxdic,multialignment='left')
                plt.savefig(histfileP)
                plt.close()
                
                print(f'[{md}/{grp}] Euclid distance of Symm_Func is plotted')

    #Plot scatter of TC err & L2 norm based on Train symm_func            
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(f'[{md}] TC err & Mean of Symm_Func L2 (Train base)')
    ax.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax.set_ylabel("Mean of Predict Symm_Func L2 norm")
    ax.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for SFL2T in SFL2TTC:
        ax.scatter(SFL2T[1], SFL2T[0], c=SFL2T[2], marker='.')
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
        ax4.scatter(SFL2T[1], SFL2T[0],c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax.legend(handler4, label4,loc='lower right',title='LC grp')
    fig.delaxes(ax4)
    plt.savefig(plotfileT)
    plt.close()

    #Plot scatter of TC err & L2 norm based on Predict symm_func            
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(f'[{md}] TC err & Mean of Symm_Func L2 (Predict base)')
    ax.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax.set_ylabel("Mean of Train Symm_Func L2 norm")
    ax.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for SFL2P in SFL2PTC:
        ax.scatter(SFL2P[1], SFL2P[0], c=SFL2P[2], marker='.')
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
        ax4.scatter(SFL2P[1], SFL2P[0],c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax.legend(handler4, label4,loc='lower right',title='LC grp')
    fig.delaxes(ax4)
    plt.savefig(plotfileP)
    plt.close()
    
    print(f'[Train-B:{len(SFL2TTC)} & Predict-B:{len(SFL2PTC)}] of L2 & TC err is plotted')
    plt.close()

def diffSymF(Tsymf,Psymf):
    #Calculate L2 norm of Symmetry Function 
    lenSFt= len(Tsymf[0][0])
    SFdtt= Tsymf.reshape(-1,lenSFt)
    SFt_mean= SFdtt.mean(axis=0, keepdims=True)

    lenSFp= len(Psymf[0][0])
    SFdtp= Psymf.reshape(-1,lenSFp)
    SFp_mean= SFdtp.mean(axis=0, keepdims=True)
    if lenSFt!=lenSFp or len(SFt_mean[0])!=lenSFt:
        print(f'PCx length error: SFt={lenSFt} SFp={lenSFp} SFt-mean={len(SFt_mean)}')
        sys.exit()

    L2T= []
    for SFp in SFdtp:
        symfdiff=SFp-SFt_mean
        #L2 norm = sqrt of sum of squares
        L2nrm=np.linalg.norm(symfdiff,ord=2)
        L2T.append(L2nrm)
        
    L2P= []
    for SFt in SFdtt:
        symfdiff=SFt-SFp_mean
        #L2 norm = sqrt of sum of squares
        L2nrm=np.linalg.norm(symfdiff,ord=2)
        L2P.append(L2nrm)

    return([L2T, L2P])

if __name__ == '__main__': 
    #calculate the diff of Lammps-MD LC7 Symm_Func of Train & Predict
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/L2-TC/"
    ph3folder="/predict-phono3py-3"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,ph3folder,grps,"Lammps-MD-LC7")
    
    #calculate the diff of AIMD LC7 Symm_Func of Train & Predict
    root="/home/okugawa/HDNNP/Si-190808-md/"
    LC7root=root+"1000K-LC7n/"
    outfolder=root+"result-LC7n/L2-TC/"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    ph3folder="/predict-phono3py"
    plotL2TC(LC7root,outfolder,ph3folder,grps,"AIMD-LC7") 