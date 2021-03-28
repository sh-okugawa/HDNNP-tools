# -*- coding: utf-8 -*-
import sys
import re
import csv
import matplotlib.pyplot as plt

"""
This script is for plotting each data (force/RMSE & TC(300K) diff from 112.1) 
with classified color by normalized distance
"""

def plotdata(rstfile, plotfile, grp, grp2, dn):
    dlabels=['data=70','data=175','data=350','data=700','data=1400',
             'data=2100','data=2800','data=3500']
    nlabels=['node=50','node=100','node=200','node=300','node=500']
    dcolors=["red","orange","pink","lime","cyan","deepskyblue","b","darkgreen"]
    ncolors=["red","orange","green","cyan","b"]
    grplen=len(grp)
    
    if dn=='d':
        ttl='data'
        labels=dlabels
        colors=dcolors
    elif dn=='n':
        ttl='node'
        labels=nlabels
        colors=ncolors
    else:
        print(f'Error: Invalid parameter of plotdata(dn)')
        sys.exit()    

    with open(rstfile, 'r') as rslt:
        readcsv = csv.reader(rslt)
        RMSETC = []

        for row in readcsv:
            gnameall = re.split('[dn-]',row[0])
            if dn=='d':
                gname= gnameall[1]
                if gname in grp:
                    clr=colors[grp.index(gname)]
                    RMSETC.append([float(row[1]),abs(float(row[2])),clr])
            else:
                gname= gnameall[2]
                if gname in grp and gnameall[1] in grp2:
                    clr=colors[grp.index(gname)]
                    RMSETC.append([float(row[1]),abs(float(row[2])),clr])
            
    #Plotting all sample of force/RMSE and TC error for each group
    samplenum= len(RMSETC)
    print("Plotting all of %s sample (%d)" % (dn, samplenum))
    plottitle="All type of "+ttl
    fig = plt.figure()
    ax3 = fig.add_subplot(111)
    plt.title(plottitle)
    ax3.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax3.set_ylabel("force/RMSE (meV/A)")
    ax3.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
                
    for dtn in range(samplenum):
        ax3.scatter(RMSETC[dtn][1],RMSETC[dtn][0],c=RMSETC[dtn][2],marker='.',s=20)

    left, right = ax3.get_xlim()
    ax3.set_xlim(-0.1, right*1.2)
    #ax4 is only for plotting legend of all kind of data
    ax4 = ax3.twinx()
    for j in range(grplen):
        lbl=labels[j]
        clr=colors[j]
        ax4.scatter(RMSETC[0][1],RMSETC[0][0],c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax3.legend(handler4, label4,loc='upper right',title='Sample grp',
               bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax4)
    plt.savefig(plotfile)
    plt.close()    
    
    
if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/Si-190808"

    tdata=["2","5","10","20","40","60","80","100"]
    t2data=["20","40","60","80","100"]
    node=["50","100","200","300","500"]
    rstfile=root+"/result/RMSETCdata.csv"
    plotdir=root+"/result/grpplot/opt/"
   
    #Plotting all data# sample of nxx
    plotfile=plotdir+"all-data.png"
    plotdata(rstfile, plotfile, tdata, t2data, "d")

    #Plotting all node# sample of dxx
    plotfile=plotdir+"all-node.png"
    plotdata(rstfile, plotfile, node, t2data, "n")