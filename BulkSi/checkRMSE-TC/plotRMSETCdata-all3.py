# -*- coding: utf-8 -*-
import sys
import re
import csv
import matplotlib.pyplot as plt

"""
This script is for plotting each node# (force/RMSE & TC(300K) diff from 112.1) 
with classified color of each data#
"""

def plotRMSETC(RMSETC,plotdir,dn,colors):
    dlabels=['70','175','350','700','1400','2100','2800','3500']
    nlabels=['50','100','200','300','500']

    if dn=="node":
        labels=dlabels
        lblhead='data='
        filenm=nlabels
    elif dn=="data":
        labels=nlabels
        lblhead='node='
        filenm=dlabels
    else:
        print(f'dn parameter error: dn={dn}')
        sys.exit()
    
    #Plotting all sample of force/RMSE and TC error for all node# group
    plotfile=plotdir+dn+"all-all.png"
    plottitle="[All "+dn+"#] Scatter of Force/RMSE & TC err"
    fig = plt.figure()
    ax3 = fig.add_subplot(111)
    plt.title(plottitle)
    ax3.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax3.set_ylabel("force/RMSE (meV/A)")
    ax3.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
                
    for i in range(len(filenm)):
        for dtn in RMSETC[i]:
            ax3.scatter(dtn[1],dtn[0],c=dtn[2],marker='.',s=20)

    left, right = ax3.get_xlim()
    bottom, top = ax3.get_ylim()
    ax3.set_xlim(-0.1, right*1.2)
    #ax4 is only for plotting legend of all kind of data
    ax4 = ax3.twinx()
    for j in range(len(labels)):
        lbl=lblhead+labels[j]
        clr=colors[j]
        ax4.scatter(dtn[1],dtn[0],c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax3.legend(handler4, label4,loc='upper right',title='Sample grp',
               bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax4)
    plt.savefig(plotfile)
    plt.close() 
    print(f'All of all-{dn}# sample is plotted') 
          
    #Plotting all sample of force/RMSE and TC error for each node# group
    for i,fn in enumerate(filenm):
        plotfile=plotdir+dn+fn+"-all.png"
        plottitle="["+dn+"="+fn+"] Scatter of Force/RMSE & TC err"
        fig = plt.figure()
        ax3 = fig.add_subplot(111)
        plt.title(plottitle)
        ax3.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
        ax3.set_ylabel("force/RMSE (meV/A)")
        ax3.grid(True)
        plt.rcParams["legend.edgecolor"] ='green'
                    
        for dtn in RMSETC[i]:
            ax3.scatter(dtn[1],dtn[0],c=dtn[2],marker='.',s=20)
    
        ax3.set_xlim(-0.1, right*1.2)
        ax3.set_ylim(bottom, top)
        #ax4 is only for plotting legend of all kind of data
        ax4 = ax3.twinx()
        for j in range(len(labels)):
            lbl=lblhead+labels[j]
            clr=colors[j]
            ax4.scatter(dtn[1],dtn[0],c=clr,marker='.',label=lbl)
        handler4, label4 = ax4.get_legend_handles_labels()
        ax3.legend(handler4, label4,loc='upper right',title='Sample grp',
                   bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
        fig.delaxes(ax4)
        plt.savefig(plotfile)
        plt.close() 
        print(f'All of {dn}-{fn} sample is plotted')     

if __name__ == '__main__': 
    datagrp=["2","5","10","20","40","60","80","100"]
    nodegrp=["50","100","200","300","500"]
    dcolors=["red","orange","pink","lime","cyan","deepskyblue","b","darkgreen"]
    ncolors=["red","orange","green","cyan","b"]
    
    root="/home/okugawa/HDNNP/Si-190808"
    rstfile=root+"/result/RMSETCdata.csv"
    plotdir=root+"/result/grpplot/opt-node/"
   
    #Read RMSETC.csv and make list of plotting data for each node#
    with open(rstfile, 'r') as rslt:
        readcsv = csv.reader(rslt)
        RMSETCd = [[] for i in range(len(nodegrp))]
        RMSETCn = [[] for i in range(len(datagrp))]

        for row in readcsv:
            gnameall = re.split('[dn-]',row[0])
            dname= gnameall[1]
            nname= gnameall[2]
            if not dname in datagrp and nname in nodegrp:
                print(f'RMSETC data error: data=[{dname}] & node=[{nname}]')
                sys.exit()
            dclr=dcolors[datagrp.index(dname)]
            nodenum=nodegrp.index(nname)
            RMSETCd[nodenum].append([float(row[1]),abs(float(row[2])),dclr])
            nclr=ncolors[nodegrp.index(nname)]
            datanum=datagrp.index(dname)
            RMSETCn[datanum].append([float(row[1]),abs(float(row[2])),nclr])
            
    plotRMSETC(RMSETCd,plotdir,"node",dcolors)
    plotRMSETC(RMSETCn,plotdir,"data",ncolors)