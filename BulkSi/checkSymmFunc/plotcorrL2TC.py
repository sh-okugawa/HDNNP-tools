# -*- coding: utf-8 -*-
import re
import csv
import numpy as np
import matplotlib.pyplot as plt

"""
This script is calculating the Euclid distance (L2 norm) 
between Symmetry Function of Train and Predict,
then plot scatter of L2 norm mean and TC err 
"""

def plotL2TC(LC7root, TCerrdt, outfolder, grps, md):
    colors=["purple","orange","pink","lime","cyan","deepskyblue","b","red"]
    plotfile=outfolder+"Corr-SFL2&TC.png"
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(f'[{md}] TC err & Mean of L2 norm')
    ax.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax.set_ylabel("Mean of L2 norm")
    ax.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    
    minL2=10000
    for grpnum,grp in enumerate(grps):
        clr=colors[grpnum]
        grpmin=10000
        for i in range(1,10):
            datadir=LC7root+grp+"/"+str(i)
            if grp=='mix':
                datadir=datadir+"/1"
            
            #Calculate L2 norm of Symmetry_Func diff
            symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
            symt= np.load(symfft)
            symdtt= symt['sym_func']
            symffp=datadir+"/predict-phono3py-2/output-phono3py/symmetry_function-pred.npz"
            symp= np.load(symffp)
            symdtp= symp['sym_func']
            diffSF=diffSymF(symdtt, symdtp)
            if diffSF[1] < grpmin:
                grpmin=diffSF[1]
    
            #Read TC err 
            TCerr=TCerrdt[grps.index(grp)][i]
    
            #Plot histgram of diff and report its ave and number of same-
            ax.scatter(TCerr,diffSF[0],c=clr,marker='.')

        if grpmin < minL2:
            minL2=grpmin
        print(f'Minimum of {md}-{grp} L2 norm is [{grpmin}]')
        
    print(f'Minimum of all L2 norm is [{minL2}]')
    left, right = ax.get_xlim()
    ax.set_xlim(-0.1, right*1.2)
    #ax4 is only for plotting legend of all kind of data
    ax4 = ax.twinx()
    for i,grp in enumerate(grps):
        lbl="LC="+grp
        clr=colors[i]
        ax4.scatter(TCerr,diffSF[0],c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax.legend(handler4, label4,loc='upper right',title='Sample grp',
               bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
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
    
def diffSymF(Tsymf,Psymf):
    #Calculate L2 norm of Symmetry Function difference of corresponded atom#
    totave=np.empty(0)
    totmin=10000
    for Tsym in Tsymf:
        Psave=np.empty(0)
        for Psym in Psymf:
            L2Ts=np.empty(0)
            for i,Ts in enumerate(Tsym):
                Ps= Psym[i]
                symfdiff=Ts-Ps
                #L2 norm = sqrt of sum of squares
                L2nrm=np.linalg.norm(symfdiff,ord=2)
                L2Ts= np.append(L2Ts, L2nrm)
            aves=np.mean(L2Ts)
            mins=np.min(L2Ts)
            if mins < totmin:
                totmin=mins
            Psave=np.append(Psave,aves)
        totave=np.append(totave,np.mean(Psave))
    return([np.mean(totave),totmin])

if __name__ == '__main__': 
    #calculate the diff of Lammps-MD LC7 Symm_Func of Train & Predict
    root="/home/okugawa/HDNNP/Si-190808/"
    LC7root=root+"1000K-LC7/"
    outfolder=root+"result-LC7/L2-TC/"
    rstfile=root+"result-LC7/RMSETCdata.csv"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    TCerrdt=readTCerr(rstfile, grps)
    plotL2TC(LC7root,TCerrdt,outfolder,grps,"Lammps-MD-LC7")
    
    #calculate the diff of AIMD LC7 Symm_Func of Train & Predict
    root="/home/okugawa/HDNNP/Si-190808-md/"
    LC7root=root+"1000K-LC7n/"
    outfolder=root+"result-LC7n/L2-TC/"
    rstfile=root+"result-LC7n/RMSETCdata.csv"
    grps2=['0.95','0.97','0.99','1.0','1.01','1.03','1.05','mix']
    TCerrdt=readTCerr(rstfile, grps)
    plotL2TC(LC7root,TCerrdt,outfolder,grps2,"AIMD-LC7")    