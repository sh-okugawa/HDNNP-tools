# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

"""
This script is for plotting KDE chart of PC1/PC2/PC3
of MD 1000K-LCx3 sample
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
    mdfolder=root+"Si-190808-md/"
    PCfolder=mdfolder+"/result-LC/PC123/"
    grps=['1000K0.99', '1000K1.0', '1000K1.01']

    #Plot KDE chart of MD 1000K-LCx3
    for grp in grps:
        for j in range(1,11):
            grpname=grp+"-"+str(j)
            PCfile=PCfolder+grp+"-"+str(j)+"-PC123.txt"
            plotfile=PCfolder+"KDE/"+grpname+"-K.png"
            plotKDE(PCfile,plotfile,grpname)
             
    #Plot KDE chart of gs
    PCfile=root+"Si-190808/result/PC123/PC123-d20.txt"
    plotfile=PCfolder+"KDE/gs-K.png"
    plotKDE(PCfile,plotfile,"gs")    