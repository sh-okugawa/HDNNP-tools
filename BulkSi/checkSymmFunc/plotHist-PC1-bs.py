# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np

"""
This script is for plotting Histgram chart of PC1 of MD 1000K-LCx4
"""

def plotHIST(PCfile,plotfile,grpname):
    PC123dt = np.loadtxt(PCfile, dtype="float")
    PC1=[]
    for PC123 in PC123dt:
        PC1.append(PC123[0])

    #Plot KDE chart of PC1/PC2 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plttitle="["+grpname+"] PC1 Histgram"
    plt.title(plttitle)
    plt.ylim(0, 6000)
    plt.hist(PC1, bins=100, range=(-2.3, 2.3))

    plt.savefig(plotfile)
    print(f'PC1 histgram of {grpname} is plotted')
    plt.close('all')

if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/"
    bsfolder=root+"Si-190808-bs/"
    PCfolder=bsfolder+"/result/PC123/"
    grps=["bs1","bs2","bs3","bs4","bs5","bs6","bs7","bs8"]

    #Plot KDE chart of bs1-8
    for grp in grps:
        PCfile=PCfolder+grp+"-PC123.txt"
        plotfile=PCfolder+"HIST/"+grp+".png"
        plotHIST(PCfile,plotfile,grp)
             
    #Plot Violin chart of gs
    PCfile=root+"Si-190808/result/PC123/PC123-d20.txt"
    plotfile=PCfolder+"HIST/gs.png"
    plotHIST(PCfile,plotfile,"gs")    