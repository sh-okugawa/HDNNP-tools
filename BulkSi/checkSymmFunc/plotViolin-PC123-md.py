# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns

"""
This script is for plotting Violin chart of PC1/PC2/PC3
of MD 1000K/1200K sample
"""

def plotViolin(PCfile,plotfile,grpname):
    with open(PCfile, 'r') as f1:
        PCdt=[[],[],[]]
        for line in f1:
            linesp=line.split()
            for i in range(3):
                PCdt[i].append(float(linesp[i]))
                      
    #Plot Violin chart of G1/G4-1/G4-5 
    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    sns.set_palette('gray')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plttitle="["+grpname+"] Violin chart of PC1/PC2/PC3"
    plt.title(plttitle)
    ax.violinplot([PCdt[0],PCdt[1],PCdt[2]])
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["PC1","PC2","PC3"])
    ax.set_ylabel("Value of PC")

    plt.savefig(plotfile)
    print(f'Violin chart of {grpname} is plotted')
    plt.close()

if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/"
    mdfolder=root+"Si-190808-md/"
    PCfolder=mdfolder+"/result/PC123/"
    grps=['1000K','1200K']

    #Plot Violin chart of MD 1000K/1200K
    for grp in grps:
        for j in range(1,11):
            grpname=grp+"-"+str(j)
            PCfile=PCfolder+grp+"-"+str(j)+"-PC123.txt"
            plotfile=PCfolder+"violin/"+grpname+"-V.png"
            plotViolin(PCfile,plotfile,grpname)
             
    #Plot Violin chart of gs
    PCfile=root+"Si-190808/result/PC123/PC123-d20.txt"
    plotfile=PCfolder+"violin/gs-V.png"
    plotViolin(PCfile,plotfile,"gs")    