# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

"""
This script is for plotting G1/G2/G4 data of calculated Symm-Func
of MD 1000K/1200K sample
"""

if __name__ == '__main__': 
    mdfolder="/home/okugawa/HDNNP/Si-190808-md/"
    outfolder=mdfolder+"/result/symf/"
    grps=['1200K']

    xlb=["G1"]
    clr=["b"]
    for i in range(1, 25):
        xlb.append("G2-"+str(i))
        clr.append("g")
    for i in range(1, 17):
        xlb.append("G4-"+str(i))
        clr.append("c")

    for grp in grps:
        symdataall=[]
        for j in range(1,11):
            grpname=grp+"-"+str(j)
            symffile=mdfolder+grp+"/"+str(j)+"/data/CrystalSi64/symmetry_function.npz"
            plotfile=outfolder+grp+"/"+grpname+"-Gdata.png"

            symf= np.load(symffile)
            symdata= symf['sym_func']
            symdataall.append(symdata)

            #Plot G-data of each group 
            fig = plt.figure()
            ax = fig.add_subplot(111)
            plttitle="["+grpname+"] Symmetry_Function (G1/G2/G4) data"
            plt.title(plttitle)
            ax.set_ylabel("Value of G")
            ax.grid(True)
                      
            for eachsample in symdata:
                for gdata in eachsample:
                    ax.scatter(xlb, gdata, c=clr, marker='.')
                    
            labels = ax.get_xticklabels()
            plt.setp(labels, rotation=90, fontsize=8);
            plt.savefig(plotfile)
            print(f'G-data of {grpname} is plotted')
            plt.close()

        #Plot G-data of all group 
        plotallfile=outfolder+grp+"/"+grp+"-all-Gdata.png"
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plttitle="["+grp+"-all] Symmetry_Function (G1/G2/G4) data"
        plt.title(plttitle)
        ax.set_ylabel("Value of G")
        ax.grid(True)
        
        for symdata in symdataall:
            for eachsample in symdata:
                for gdata in eachsample:
                    ax.scatter(xlb, gdata, c=clr, marker='.')
                    
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=8);
        plt.savefig(plotfile)
        print(f'G-data of {grp}-all is plotted')
        plt.close()