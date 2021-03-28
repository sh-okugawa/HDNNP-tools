# -*- coding: utf-8 -*-
import os
import csv
import matplotlib.pyplot as plt

"""
This script is for plotting each data (force/RMSE & TC(300K) diff from 112.1) 
with classified color by normalized distance
"""

def plotdata(rstfile, plotfile, grp, m, dn):
    labels=('nrm>0.9','0.9>nrm>0.6','0.6>nrm>0.4','0.4>nrm>0.2','0.2>nrm>0.1','0.1>nrm')
    colors=("red","orange","yellow","cyan","c","b")
    
    with open(rstfile, 'r') as rslt:
        readcsv = csv.reader(rslt)
        RMSETC = []

        for row in readcsv:
            gnameall = row[0]
            gname = gnameall.split("-")[0]
            if gname in grp:
                normalized = float(row[3])
                if normalized>0.9:
                    RMSETC.append([float(row[1]),float(row[2]),colors[0]])
                elif normalized>0.6:
                    RMSETC.append([float(row[1]),float(row[2]),colors[1]])
                elif normalized>0.4:
                    RMSETC.append([float(row[1]),float(row[2]),colors[2]])
                elif normalized>0.2:
                    RMSETC.append([float(row[1]),float(row[2]),colors[3]])
                elif normalized>0.1:
                    RMSETC.append([float(row[1]),float(row[2]),colors[4]])
                else:
                    RMSETC.append([float(row[1]),float(row[2]),colors[5]])
            
    #Plotting all sample of force/RMSE and TC error for each group
    samplenum= len(RMSETC)
    print("Plotting all of %s%s sample (%d)" % (dn, m, samplenum))
    plottitle="d20-100 of "+dn+m+" samples"
    fig = plt.figure()
    ax3 = fig.add_subplot(111)
    plt.title(plottitle)
    ax3.set_xlabel("TC Err (fm 112.1)")
    ax3.set_ylabel("force/RMSE (meV/A)")
    ax3.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
                
    for dtn in range(samplenum):
        ax3.scatter(RMSETC[dtn][1],RMSETC[dtn][0],c=RMSETC[dtn][2],marker='.')

    left, right = ax3.get_xlim()
    ax3.set_xlim(-0.1, right*1.2)
    #ax4 is only for plotting legend of all kind of data
    ax4 = ax3.twinx()
    for j in range(0, 6):
        lbl=labels[j]
        clr=colors[j]
        ax4.scatter(RMSETC[0][1],RMSETC[0][0],c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax3.legend(handler4, label4,loc='upper right',title='Normalized dist',bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax4)
    plt.savefig(plotfile)
    plt.close()    
    
    
if __name__ == '__main__': 
    root=os.getcwd()

    tdata=["20","40","60","80","100"]
    node=["50","100","200","300","500"]
    rstfile=root+"/result/RMSEdata.csv"
    plotdir=root+"/result/grpplot/opt/"
   
    #Plotting all data# sample of nxx
    for i in node:
        grp = []
        plotfile=plotdir+"n"+i+"all-2.png"
        for k in tdata:
            grpname="d"+k+"n"+i
            grp.append(grpname)
        plotdata(rstfile, plotfile, grp, i, "n")
