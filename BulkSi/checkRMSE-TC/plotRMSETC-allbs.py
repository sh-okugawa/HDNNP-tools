# -*- coding: utf-8 -*-
import os
import csv
import ast
from itertools import islice
import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy

"""
This script is plotting force/RMSE and TC error of all bad sample data 
"""
if __name__ == '__main__': 
    root=os.getcwd()

    bsxs=["bs1","bs2","bs3","bs4","bs5","bs6","bs7","bs8"]

    rstfile=root+"/result/RMSEdata.csv"
    plotdir=root+"/result/grpplot/"
    labels=('nrm>0.9','0.9>nrm>0.6','0.6>nrm>0.4','0.4>nrm>0.2','0.2>nrm>0.1','0.1>nrm')
    colors=("red","pink","orange","yellow", "green","cyan","c","b")

    with open(rstfile, 'r') as rslt:
        readcsv = csv.reader(rslt)
        RMSETC = []
        for row in readcsv:
            RMSETC.append([float(row[1]),float(row[2])])

    #Plotting all data of correlation of force/RMSE and TC error
    dtn=0
    allplotfile=plotdir+"alldata-bs.png"
    fig = plt.figure()
    ax3 = fig.add_subplot(111)
    plt.title("All data")
    ax3.set_xlabel("TC Err (fm 112.1/300K)")
    ax3.set_ylabel("force/RMSE (meV/A)")
    ax3.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
            
    for i, bsx in enumerate(bsxs):
        for j in range(0, 10):
            ax3.scatter(RMSETC[dtn][1],RMSETC[dtn][0],c=colors[i],marker='.')
            dtn=dtn+1

    left, right = ax3.get_xlim()
    ax3.set_xlim(-0.1, right*1.2)

    #ax4 is only for plotting legend of all kind of data
    ax4 = ax3.twinx()
    for i, bsx in enumerate(bsxs):
        ax4.scatter(RMSETC[0][1],RMSETC[0][0],c=colors[i],marker='.',label=bsx)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax3.legend(handler4, label4,loc='upper right',title='Sample Grp',bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax4)
    plt.savefig(allplotfile)
    plt.close()
    