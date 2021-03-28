# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

"""
This script is for plotting G1/G2/G4 data of calculated Symm-Func for
train and predict of Lammps-MD 1000K LC7 
"""

def plotG(symdt, plttitle, plotfile, xlb, clr):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(plttitle)
    ax.set_ylabel("Value of G")
    ax.grid(True)
    
    num=0    
    for symdata in symdt:
        for eachsample in symdata:
            print(f'{num}: {plttitle}')
            for gdata in eachsample:
                ax.scatter(xlb, gdata, c=clr, marker='.')
                num=num+1
                
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8);
    plt.savefig(plotfile)
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
        symdtt, symdtp = [],[]
        plotfileT=outfolder+grp+"-Gdata-T.png"
        plotfileP=outfolder+grp+"-Gdata-P.png"
        for i in range(1, 11):
            if grp=='mix':
                for j in range(1, 11):
                    datadir=root+grp+"/"+str(i)+"/"+str(j)
                    symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
                    symt= np.load(symfft)
                    symdata= symt['sym_func']
                    symdtt.append(symdata)
                    symffp=datadir+"/predict-phono3py-2/output-phono3py/symmetry_function-pred.npz"
                    symp= np.load(symffp)
                    symdata= symp['sym_func']
                    symdtp.append(symdata)
            else:
                datadir=root+grp+"/"+str(i)
                symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
                symt= np.load(symfft)
                symdata= symt['sym_func']
                symdtt.append(symdata)
                symffp=datadir+"/predict-phono3py-2/output-phono3py/symmetry_function-pred.npz"
                symp= np.load(symffp)
                symdata= symp['sym_func']
                symdtp.append(symdata)
        print(f'Symm_func of {grp} is gathered')

        stnparr=np.array(symdtt)
        plttitle=f'[{md}/{grp}] Train({stnparr.shape}) Symm_Func G value'
        plotG(symdtt, plttitle, plotfileT, xlb, clr)
        spnparr=np.array(symdtp)
        plttitle=f'[{md}/{grp}] Predict({spnparr.shape}) Symm_Func G value'
        plotG(symdtp, plttitle, plotfileP, xlb, clr)        
        print(f'Symm_func of {grp} is plotted')
        
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