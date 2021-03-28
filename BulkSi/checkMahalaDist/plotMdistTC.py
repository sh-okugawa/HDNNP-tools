# -*- coding: utf-8 -*-
import re,sys
import csv
import numpy as np
import scipy.spatial.distance as SSD
import matplotlib.pyplot as plt

"""
This script is calculating Mahalanobis distance of each predict's symm_func
then plot scatter of M-dist mean and TC err 
"""

def plotL2TC(LC7root, TCerrdt, outfolder, grps, md):
    colors=["purple","orange","pink","lime","cyan","green","b","red"]
    plotfile=outfolder+"TCe&MD.png"

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for grpnum,grp in enumerate(grps):
        clr=colors[grpnum]
        for i in range(1,10):
            datadir=LC7root+grp+"/"+str(i)
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

            #Read TC err 
            TCerr=TCerrdt[grps.index(grp)][i]
    
            #Plot scatter of TC err & ave of Mahalanobis distance
            ax.scatter(TCerr,MDave,c=clr,marker='.')

        print(f'[{md}/{grp}] TC err & Ave of Mahalanobis distance is plotted')
        
    plt.title(f'[{md}] TC err & Mean of Mahalanobis distance')
    ax.set_xlabel(f'TC Err (fm 112.1W/m-K:300K)')
    ax.set_ylabel(f'Mean of Mahalanobis dist ({lenSFp} symm_func)')
    ax.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
  
    left, right = ax.get_xlim()
    ax.set_xlim(-1, right*1.2)
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
        ax4.scatter(TCerr,MDave,c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax.legend(handler4, label4,loc='lower right',title='LC grp')
    fig.delaxes(ax4)
    plt.savefig(plotfile)
    plt.close()

def readTCerr(rstfile, grps):
    #Read TC err from csv file
    with open(rstfile, 'r') as rslt:
        readcsv = csv.reader(rslt)
        TCerrdt = [[] for i in range(len(grps))]
        for row in readcsv:
            gnameall = re.split('[-]',row[0])
            LC= gnameall[1]
            TCerrdt[grps.index(LC)].append(abs(float(row[2])))
    return(TCerrdt)

if __name__ == '__main__': 
    #calculate Mahalanobis distance of Lammps-MD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/Mdist/"
    rstfile=root+"result-LC7/RMSETCdata.csv"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    TCerrdt=readTCerr(rstfile, grps)
    plotL2TC(LC7root,TCerrdt,outfolder,grps,"Lammps-MD-LC7")
    
    #calculate Mahalanobis distance of AIMD LC7 Symm_Func and plot
    root="/home/okugawa/HDNNP/Si-190808-md/"
    LC7root=root+"1000K-LC7n/"
    outfolder=root+"result-LC7n/Mdist/"
    rstfile=root+"result-LC7n/RMSETCdata.csv"
    AIgrps=['0.95','0.97','0.99','1.0','1.01','1.03','1.05','mix']
    TCerrdt=readTCerr(rstfile, grps)
    plotL2TC(LC7root,TCerrdt,outfolder,AIgrps,"AIMD-LC7")