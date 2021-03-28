# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

"""
This script is for plotting Hex-Heatmap of PC1/PC2 and Histgram of PC1 
of MD 1000K-LCx4 and 1000K/1200K
"""

def plotHIST(PCfile,HMplotfile,HISTplotfile,grpname):
    PC123dt = np.loadtxt(PCfile, dtype="float")
    PC1,PC2 =[],[]
    for PC123 in PC123dt:
        PC1.append(PC123[0])
        PC2.append(PC123[1])

    #Plot Hex-Heatmap with histgram of PC1/PC2 
    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    plttitle="["+grpname+"]"
    ax = sns.jointplot(x=PC1, y=PC2, kind='hex', xlim=(-2.5, 2.5), ylim=(-0.3, 0.35))
    plt.text(-10, 0.24, plttitle, size = 15, color = "black")
    plt.savefig(HMplotfile)
    plt.close('all')
    
    #Plot Histgram of PC1 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plttitle="["+grpname+"] PC1 Histgram"
    plt.title(plttitle)
    plt.ylim(0, 6000)
    plt.hist(PC1, bins=100, range=(-2.3, 2.3))
    plt.savefig(HISTplotfile)
    plt.close('all')

if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/"
    bsfolder=root+"Si-190808-md/"
    PCfolder=bsfolder+"/result/PC123/"
    grps=['1000K0.99','1000K1.0','1000K1.01','1000Kmix','1000K','1200K']

    #Plot Histgram chart of MD 1000K-LCx4 and 1000K/1200K
    for grp in grps:
        for j in range(1,11):
            grpname=grp+"-"+str(j)
            PCfile=PCfolder+grpname+"-PC123.txt"
            HMplotfile=PCfolder+"HIST/"+grpname+"-HEX.png"
            HISTplotfile=PCfolder+"HIST/"+grpname+"-H.png"
            plotHIST(PCfile,HMplotfile,HISTplotfile,grpname)
        print(f'HexHeatmap and Histgram of {grp} is plotted')
