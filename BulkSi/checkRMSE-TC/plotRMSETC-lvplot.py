# -*- coding: utf-8 -*-
import os
import csv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

"""
This script is for plotting each data (force/RMSE & TC(300K) diff from 112.1) 
with classified color by normalized distance
"""

if __name__ == '__main__': 
    root=os.getcwd()
    rstfile=root+"/result/RMSEdata.csv"
    plotdir=root+"/result/grpplot/opt/"
    dngrp=["d2","d5","d10"]

    with open(rstfile, 'r') as rslt:
        readcsv = csv.reader(rslt)
        RMSETC = []
        RMSETCn = []

        for row in readcsv:
            gnameall = row[0]
            gname = gnameall.split("-")[0]
            dname = gname.split("n")[0]
            nname = "n"+gname.split("n")[1]
            RMSETC.append([dname, nname, row[1], "RMSE"])
            RMSETC.append([dname, nname, row[2], "TC"])
            if not dname in dngrp:
                RMSETCn.append([dname, nname, row[1], "RMSE"])
                RMSETCn.append([dname, nname, row[2], "TC"])
            
    RMSETCpd = pd.DataFrame(RMSETC, columns=["data","node","forceRMSE/TC","RoT"])
    RMSETCnpd = pd.DataFrame(RMSETCn, columns=["data","node","forceRMSE/TC","RoT"])
    
    fig = plt.figure()
    ax3 = fig.add_subplot(111)
    plt.title("force/RMSE & TC for each data#")
    ax = sns.boxplot(x="data", y="forceRMSE/TC", hue="RoT", data=RMSETCpd)
    ax.legend(loc='upper right')
    ax.grid()
    plotfile=plotdir+"lvplot-data.png"
    plt.savefig(plotfile)
    
    fig = plt.figure()
    ax3 = fig.add_subplot(111)
    plt.title("force/RMSE & TC for each node#")
    ax = sns.boxplot(x="node", y="forceRMSE/TC", hue="RoT", data=RMSETCnpd)
    ax.legend(loc='upper right')
    ax.grid()
    plotfile=plotdir+"lvplot-node.png"
    plt.savefig(plotfile)   
    plt.close()