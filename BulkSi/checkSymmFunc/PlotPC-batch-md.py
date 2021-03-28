# -*- coding: utf-8 -*-
import os, sys
import numpy as np
import matplotlib.pyplot as plt

"""
This script is for standardizing PC1&PC2&PC3 data 
and plot scatter of standardized PC1&PC2
"""

if __name__ == '__main__': 
    mdfolder="/home/okugawa/HDNNP/Si-190808-md"
    outfolder=mdfolder+"/result/PC123/"
    args=sys.argv
    grpname= args[1]
    j= args[2]
    PCdtdir=mdfolder+"/result/PC123/"
    plotdir=PCdtdir+"plot/"
    
    PCdatafile=PCdtdir+grpname+"-"+str(j)+"-PC123.txt"
    PCdt = np.loadtxt(PCdatafile)
    
    ### plot scatter of inputs/0 PC1&PC2
    fig = plt.figure()
    ax2 = fig.add_subplot(111)
    plottitle2="["+grpname+"-"+str(j)+"] "+"PC1 & PC2"
    plt.title(plottitle2)
    
    ax2.set_xlabel("PC1")
    ax2.set_ylabel("PC2")
    ax2.grid(True)
    
    for dt in PCdt:
        ax2.scatter(dt[0],dt[1],marker='.')
    plotfile=plotdir+grpname+"-"+str(j)+"-PC1PC2.png"
    plt.savefig(plotfile)
    print(f'PC1PC2 scatter of {grpname}-{j} is plotted')
    plt.close() 