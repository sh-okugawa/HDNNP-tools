# -*- coding: utf-8 -*-
import sys
import numpy as np
from itertools import islice
from sklearn import linear_model
import matplotlib.pyplot as plt

"""
This script is calculating Euclid distance (L2 norm) of each predict's Symm_Func
and also PCx then plot scatter of L2 norm mean and TC err with coef/R^2/corr data
"""

def plotL2TC(LC7root, outfolder, ph3folder, grps, md):
    colors=["purple","orange","pink","lime","cyan","green","b","red"]
    SFL2tTC,SFL2pTC,SFL2tTCcoef,SFL2pTCcoef= [],[],[],[]
    PCxL2tTC,PCxL2pTC,PCxL2tTCcoef,PCxL2pTCcoef= [],[],[],[]
    L2TCerr,L2TCerrL= [],[]

    for grpnum,grp in enumerate(grps):
        clr=colors[grpnum]
        
        for i in range(1,11):
            datadir=LC7root+grp+"/"+str(i)
            if grp=='mix':
                datadir=datadir+"/1"
            
            #Read Symmetry_Function of Train
            symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
            symt= np.load(symfft)
            symdtt= symt['sym_func']

            #Read Symmetry_Function of TC-predict
            symffp=datadir+ph3folder+"/output-phono3py/symmetry_function-pred.npz"
            symp= np.load(symffp)
            symdtp= symp['sym_func']

            SFL2=diffSymF(symdtt, symdtp)
            aveSFL2T=sum(SFL2[0])/len(SFL2[0])
            aveSFL2P=sum(SFL2[1])/len(SFL2[1])

            #Read PCx of Train's Symmetry_Function
            dtsetfile=datadir+"/data/CrystalSi64/preprocd_dataset.npz"
            dtset= np.load(dtsetfile, allow_pickle=True)
            #allow_pickle op is for adapting spec change of numpy 1.16.3 and later
            dts= dtset['dataset']
            dts0t=[]
            for dt in dts:
                dt0t=dt['inputs/0']
                dts0t.append(dt0t)

            #Read PCx of TC-predict's Symmetry_Function 
            pdtsetfile=datadir+ph3folder+"/output-phono3py/symmetry_function-pred-prepro.npz"
            dtsetp= np.load(pdtsetfile, allow_pickle=True)
            #allow_pickle op is for adapting spec change of numpy 1.16.3 and later
            dtsp= dtsetp['dataset']
            dts0p=[]
            for dt in dtsp:
                dt0p=dt['inputs/0']
                dts0p.append(dt0p)
                
            PCxL2=diffSymF(dts0t, dts0p)
            avePCxL2T=sum(PCxL2[0])/len(PCxL2[0])
            avePCxL2P=sum(PCxL2[1])/len(PCxL2[1])

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
    
            SFL2tTC.append([aveSFL2T,TCerr,clr])
            SFL2pTC.append([aveSFL2P,TCerr,clr])
            SFL2tTCcoef.append(aveSFL2T)
            SFL2pTCcoef.append(aveSFL2P)
            PCxL2tTC.append([avePCxL2T,TCerr,clr])
            PCxL2pTC.append([avePCxL2P,TCerr,clr])
            PCxL2tTCcoef.append(avePCxL2T)
            PCxL2pTCcoef.append(avePCxL2P)
            L2TCerr.append(TCerr)
            L2TCerrL.append([TCerr])

    #Plot scatter of TC err & Euclid distance based on Train symm_func            
    plotfile=outfolder+"L2-TC/SFmeanL2tTC-coef.png"
    plotcoef(plotfile,SFL2tTC,L2TCerr,L2TCerrL,SFL2tTCcoef,grps,"Symm_Func","Train",md)

    #Plot scatter of TC err & Euclid distance based on Predict symm_func            
    plotfile=outfolder+"L2-TC/SFmeanL2pTC-coef.png"
    plotcoef(plotfile,SFL2pTC,L2TCerr,L2TCerrL,SFL2pTCcoef,grps,"Symm_Func","Predict",md)
    print(f'[{md}] Train-B:{len(SFL2tTC)} & Predict-B:{len(SFL2pTC)} of SF-L2 & TC err is plotted')

    #Plot scatter of TC err & Euclid distance based on PCx of Train symm_func            
    plotfile=outfolder+"PCx/L2-TC/PCxL2tTC-coef.png"
    plotcoef(plotfile,PCxL2tTC,L2TCerr,L2TCerrL,PCxL2tTCcoef,grps,"PCx","Train",md)

    #Plot scatter of TC err & Euclid distance based on PCx of Predict symm_func            
    plotfile=outfolder+"PCx/L2-TC/PCxL2pTC-coef.png"
    plotcoef(plotfile,PCxL2pTC,L2TCerr,L2TCerrL,PCxL2pTCcoef,grps,"PCx","Predict",md)
    print(f'[{md}] Train-B:{len(PCxL2tTC)} & Predict-B:{len(PCxL2pTC)} of PCx-L2 & TC err is plotted')

def plotcoef(plotfile,DistTC,TCerr,TCerrL,L2TCcoef,grps,sp,tp,md):
    clf = linear_model.LinearRegression()
    colors=["purple","orange","pink","lime","cyan","green","b","red"]
    boxdic={"facecolor" : "lightcyan", "edgecolor" : "navy"}
    
    #Calculate coef, R^2 and corr of each sample 
    clf.fit(TCerrL,L2TCcoef)
    coefDistTC= clf.coef_[0]
    R2DistTC= clf.score(TCerrL,L2TCcoef)
    corrDistTC= np.corrcoef(TCerr,L2TCcoef)[0][1]

    #Plot scatter of TC err & distance            
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    plt.title(f'[{md}] TC err & Euclid dist of {sp} ({tp} base)')
    ax.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax.set_ylabel(f'Mean of Euclid distance of {sp}')
    ax.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for SFL2T in DistTC:
        ax.scatter(SFL2T[1], SFL2T[0], c=SFL2T[2], marker='.')
    plt.plot(TCerr, clf.predict(TCerrL))
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
    
    #Plot text box of coef, R^2, corr info
    txt1="Corr= "+str(f'{corrDistTC:.03f}')+"\n"
    txt2="Coef= "+str(f'{coefDistTC:.03f}')+"\n"
    txt3="R^2=  "+str(f'{R2DistTC:.03f}')
    coeftxt=txt1+txt2+txt3
    ax.text(0.98,0.97,coeftxt,size=10,ha='right',va='top',
     transform=ax.transAxes,bbox=boxdic,multialignment='left')
    plt.savefig(plotfile)
    plt.close()

def diffSymF(Tsymf,Psymf):
    #Calculate L2 norm of Symmetry Function 
    lenSFt= len(Tsymf[0][0])
    SFdtt= np.array(Tsymf).reshape(-1,lenSFt)
    SFt_mean= SFdtt.mean(axis=0, keepdims=True)

    lenSFp= len(Psymf[0][0])
    SFdtp= np.array(Psymf).reshape(-1,lenSFp)
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
    #calculate Mahalanobis distance of Lammps-MD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/"
    ph3folder="/predict-phono3py-3"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,ph3folder,grps,"Lammps-MD-LC7")
    
    #calculate Mahalanobis distance of AIMD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808-md/"
    LC7root=root+"1000K-LC7n/"
    outfolder=root+"result-LC7n/"
    ph3folder="/predict-phono3py"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    plotL2TC(LC7root,outfolder,ph3folder,grps,"AIMD-LC7")