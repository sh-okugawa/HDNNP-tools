# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

"""
This script is for plotting G1/G2/G4 data of calculated Symm-Func for
train and predict of Lammps-MD 1000K LC7 
"""

def plotG2(symdtt, symdtp, grp, plotfile, xlb, clr, md):
    #Plot G-data of Train 
    fig = plt.figure(figsize=(16, 4))

    ax1 = fig.add_subplot(1,2,1)
    stnparr=np.array(symdtt)
    ttl1=f'[{md}/{grp}] Train({stnparr.shape}) Symm_Func G value'
    ax1.set_title(ttl1)
    ax1.set_ylabel("Value of G")
    ax1.set_ylim(0,3.2)
    ax1.grid(True)
    for eachsample in symdtt:
        for gdata in eachsample:
            ax1.scatter(xlb, gdata, c=clr, marker='.')
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8);
    
    #Plot G-data of Predict 
    ax2 = fig.add_subplot(1,2,2)
    spnparr=np.array(symdtp)
    ttl2=f'[{md}/{grp}] Predict({spnparr.shape}) Symm_Func G value'
    ax2.set_title(ttl2)
    ax2.set_ylabel("Value of G")
    ax2.set_ylim(0,3.2)
    ax2.grid(True)
    for eachsample in symdtp:
        for gdata in eachsample:
            ax2.scatter(xlb, gdata, c=clr, marker='.')
    labels = ax2.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8);
    
    plt.savefig(plotfile)
    print(f'G-data of {grp} Train({symdtt.shape}) & Predict({symdtp.shape}) is plotted')
    plt.close()

def gatherG(root, outfolder, grps, md):
    xlb=["G1"]
    clr=["b"]
    for i in range(1, 25):
        xlb.append("G2-"+str(i))
        clr.append("g")
    for i in range(1, 17):
        xlb.append("G4-"+str(i))
        clr.append("c")

    for grp in grps:
        plotfile=outfolder+grp+"-TP-Gdata.png"
        if grp=='mix':
            datadir=root+grp+"/1/1"
        else:
            datadir=root+grp+"/1"
        symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
        symt= np.load(symfft)
        symdtt= symt['sym_func']
        symffp=datadir+"/predict-phono3py-2/output-phono3py/symmetry_function-pred.npz"
        symp= np.load(symffp)
        symdtp= symp['sym_func']

        print(f'Symm_func of {grp} is gathered')
        plotG2(symdtt, symdtp, grp, plotfile, xlb, clr, md)
        
if __name__ == '__main__': 
    #Plot Lammps-MD LC7 Symm_Func of Train & Predict
    root="/home/okugawa/HDNNP/Si-190808/1000K-LC7/"
    outfolder="/home/okugawa/HDNNP/Si-190808/result-LC7/symf/"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    gatherG(root, outfolder, grps, "Lammps-MD")
    
    #Plot AIMD LC7 Symm_Func of Train & Predict
    root="/home/okugawa/HDNNP/Si-190808-md/1000K-LC7n/"
    outfolder="/home/okugawa/HDNNP/Si-190808-md/result-LC7n/symf/"
    grps=['0.95','0.97','0.99','1.0','1.01','1.03','1.05','mix']
    gatherG(root, outfolder, grps, "AIMD") 