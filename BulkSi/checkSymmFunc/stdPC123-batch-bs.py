# -*- coding: utf-8 -*-
import os, sys
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt

"""
This script is for standardizing PC1&PC2&PC3 data 
and plot scatter of standardized PC1&PC2
"""

if __name__ == '__main__': 
    sscaler = preprocessing.StandardScaler()
    root=os.getcwd()
    args=sys.argv
    grpname= args[1]
    PCdtdir=root+"/result/PC123/"
    PCstddir=PCdtdir+"std/"
    plotdir=PCstddir+"plot/"
    
    PCdatafile=PCdtdir+grpname+"-PC123.txt"
    stdPCdatafile=PCstddir+grpname+"-PC123-std.txt"
        
    PCdt = np.loadtxt(PCdatafile)
    stdPCdt = sscaler.fit_transform(PCdt)
    np.savetxt(stdPCdatafile,stdPCdt,fmt='%.10e')
    
    ### plot scatter of inputs/0 PC1&PC2
    fig = plt.figure()
    ax2 = fig.add_subplot(111)
    plottitle2="["+grpname+"] "+"PC1 & PC2 [Standardized]"
    plt.title(plottitle2)
    
    ax2.set_xlabel("PC1")
    ax2.set_ylabel("PC2")
    ax2.grid(True)
    
    for dt in stdPCdt:
        ax2.scatter(dt[0],dt[1],marker='.')
    plotfile=plotdir+grpname+"-PC1PC2-std.png"
    plt.savefig(plotfile)
    plt.close() 