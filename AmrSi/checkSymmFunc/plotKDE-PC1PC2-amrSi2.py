# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

"""
This script is for plotting KDE chart of PC1/PC2/PC3
of Amorphous Si sample
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
    ax= sns.jointplot(data=PCdt, x='PC1', y='PC2', kind='kde')

    plt.savefig(plotfile, bbox_inches='tight')
    print(f'KDE chart of {grpname} is plotted')
    plt.close()

if __name__ == '__main__': 
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    grps=['315','1000-103040','1500-103040','1500-103040-org','1500-103040-SMZ',
          '1500-103040-Rc6.0','1500-103040-Rc7.0','1500-103040-Rc7.5']
    ttls=['315smpl-Li-Rc6.5','1000smpl-Li-Rc6.5','1500smpl-Li-Rc6.5',
          '1500smpl-org-Rc6.5','1500smpl-SMZ-Rc6.5',
          '1500smpl-Li-Rc6.0','1500smpl-Li-Rc7.0','1500smpl-Li-Rc7.5']
    sfgrps=["org","SMZ"]
    rcgrps=["6.0","7.0","7.5"]
    PCfolder=amrfolder+"/result/PC123/"

    #Plot KDE chart of MD 1000K/1200K
    for tn,grp in enumerate(grps):
        PCfile=PCfolder+grp+"-PC123.txt"
        plotfile=PCfolder+"KDE2/"+grp+"-K.png"
        plotKDE(PCfile,plotfile,ttls[tn])
             
