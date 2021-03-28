# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

"""
This script is for plotting Violin chart of G1/G4-1/G4-5
of MD 1000K/1200K sample
"""

def plotViolinPers(symffile,plotfile,grpname,persdata):
    symf= np.load(symffile)
    symdata= symf['sym_func']
    G1=[]
    G41=[]
    G45=[]

    #Gather G1/G4-1/G4-5 for plotting Violin and outputting for Persistent
    with open(persdata, 'w') as f1:
        for eachsample in symdata:
            for gdata in eachsample:
                G1.append(gdata[0])
                G41.append(gdata[25])
                G45.append(gdata[29])
                
                wdt=str(gdata[0])+" "+str(gdata[25])+" "+str(gdata[29])+"\n"
                f1.write(wdt)
            
    #Plot Violin chart of G1/G4-1/G4-5 
    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    sns.set_palette('gray')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plttitle="["+grpname+"] Violin chart of G1/G4-1/G4-5"
    plt.title(plttitle)
    ax.violinplot([G1,G41,G45])
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["G1","G4-1","G4-5"])
    ax.set_ylabel("Value of G")

    plt.savefig(plotfile)
    print(f'Violin chart of {grpname} is plotted')
    plt.close()

if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/"
    mdfolder=root+"Si-190808-md/"
    outfolder=mdfolder+"/result/symf/"
    persoutfolder=outfolder+"Pers/"
    grps=['1000K','1200K']

    #Plot Violin chart of MD 1000K/1200K
    for grp in grps:
        for j in range(1,11):
            grpname=grp+"-"+str(j)
            symffile=mdfolder+grp+"/"+str(j)+"/data/CrystalSi64/symmetry_function.npz"
            plotfile=outfolder+grp+"/"+grpname+"-V.png"
            persdata=persoutfolder+grpname+".txt"
            plotViolinPers(symffile,plotfile,grpname,persdata)
             
    #Plot Violin chart of gs
    symffile=root+"Si-190808/d20n50/1/data/CrystalSi64/symmetry_function.npz"
    plotfile=outfolder+"gs-V.png"
    persdata=persoutfolder+"gs.txt"
    plotViolinPers(symffile,plotfile,"gs",persdata)    
