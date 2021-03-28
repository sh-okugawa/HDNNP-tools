# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

"""
This script is for plotting Violin chart of PC1/PC2/PC3
of MD 1000K/1200K sample
"""

def plotKDE(PCfile,plotfile,grpname):
    PC123dt = np.loadtxt(PCfile)
    PCdt= pd.DataFrame(PC123dt, columns=['PC1','PC2','PC3'])

    #Plot KDE chart of PC1/PC2 
    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plttitle="["+grpname+"]"
    ax= sns.jointplot(data=PCdt, x='PC1', y='PC2', kind='kde', xlim=(-2.5, 2.5), ylim=(-0.3, 0.35))
    plt.text(-10, 0.24, plttitle, size = 15, color = "black")

    plt.savefig(plotfile)
    print(f'KDE chart of {grpname} is plotted')
    plt.close('all')

if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/"
    bsfolder=root+"Si-190808-bs/"
    PCfolder=bsfolder+"/result/PC123/"
    grps=["bs1","bs2","bs3","bs4","bs5","bs6","bs7","bs8"]

    #Plot KDE chart of bs1-8
    for grp in grps:
        PCfile=PCfolder+grp+"-PC123.txt"
        plotfile=PCfolder+"KDE/"+grp+"-K.png"
        plotKDE(PCfile,plotfile,grp)
             
    #Plot Violin chart of gs
    PCfile=root+"Si-190808/result/PC123/PC123-d20.txt"
    plotfile=PCfolder+"KDE/gs-K.png"
    plotKDE(PCfile,plotfile,"gs")    