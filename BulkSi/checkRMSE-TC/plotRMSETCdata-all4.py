# -*- coding: utf-8 -*-
import re
import csv
import matplotlib.pyplot as plt

"""
This script is for plotting each node# (force/RMSE & TC(300K) diff from 112.1) 
with classified color of each data#
"""

if __name__ == '__main__': 
    datagrp=["2","10","20","40","60"]
    dlabels=['70','350','700','1400','2100']
    nodegrp=["50","100","500"]
    nodemrk=["x","+","."]
    dcolors=["red","orange","lime","b","cyan"]
    
    root="/home/okugawa/HDNNP/Si-190808"
    rstfile=root+"/result/RMSETCdata.csv"
    plotfile=root+"/result/grpplot/opt-node/node-all.png"
   
    #Read RMSETC.csv and make list of plotting data for each node#
    with open(rstfile, 'r') as rslt:
        readcsv = csv.reader(rslt)
        RMSETCd = [[] for i in range(len(nodegrp))]

        for row in readcsv:
            gnameall = re.split('[dn-]',row[0])
            dname= gnameall[1]
            nname= gnameall[2]
            if dname in datagrp and nname in nodegrp:
                dclr=dcolors[datagrp.index(dname)]
                nodenum=nodegrp.index(nname)
                RMSETCd[nodenum].append([float(row[1]),abs(float(row[2])),dclr])
            
    #Plotting all sample of force/RMSE and TC error for all node# group
    plottitle="Force/RMSE & TC err of each node# and data#"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.title(plottitle, fontsize=14)
    plt.xticks(fontsize=12)  #Font size of x-axis scale
    plt.yticks(fontsize=12)  #Font size of y-axis scale
    ax.set_xlabel("TC Err (from 112.1W/m-K:300K)",fontsize=12)
    ax.set_ylabel("force/RMSE (meV/A)",fontsize=12)
    ax.grid(True)
    plt.rcParams["legend.borderpad"] ='0.3'    #Space between handle & edge
    plt.rcParams["legend.handlelength"] ='1'   #Length of handle
    plt.rcParams["legend.handletextpad"] ='0.2' #Space between handle & label
    plt.rcParams["legend.columnspacing"] ='1'  #Space between columns
    plt.rcParams["legend.labelspacing"] ='0.2' #Space between row of label
                
    for i in range(len(nodegrp)):
        lbl="node="+nodegrp[i]
        for j,dtn in enumerate(RMSETCd[i]):
            ax.scatter(dtn[1],dtn[0],c=dtn[2],marker=nodemrk[i],s=20,alpha=0.7)
   
    left, right = ax.get_xlim()
    bottom, top = ax.get_ylim()
    ax.set_xlim(-1, right*1.1)
    ax.set_ylim(bottom, top*1.1)

    #ax1 is only for plotting legend of node#
    plt.rcParams["legend.edgecolor"] ='black'
    ax1 = ax.twinx()
    for i in range(len(nodegrp)):
        lbl="node="+nodegrp[i]
        ax1.scatter(dtn[1],dtn[0],c="black",marker=nodemrk[i],label=lbl)
    handler1, label1 = ax1.get_legend_handles_labels()
    leg1=ax.legend(handler1,label1,loc='upper left',ncol=3,fontsize=12,
              facecolor="lightgray") #Legend of node#               
    fig.delaxes(ax1)
    
    #ax2 is only for plotting legend of all kind of data
    plt.rcParams["legend.edgecolor"] ='green'
    ax2 = ax.twinx()
    for j in range(len(dlabels)):
        lbl="data="+dlabels[j]
        clr=dcolors[j]
        ax2.scatter(dtn[1],dtn[0],c=clr,marker=',',label=lbl)
    handler2, label2 = ax2.get_legend_handles_labels()
    ax.legend(handler2, label2,loc='lower right',fontsize=12,
              title='Data#', title_fontsize=12)
    fig.delaxes(ax2)
    ax.add_artist(leg1)  #Write back legend of node#
    plt.savefig(plotfile)
    plt.close() 