# -*- coding: utf-8 -*-
import os
import csv
from itertools import islice
import matplotlib.pyplot as plt

"""
This script is plotting good sample and all of bad sample data with 
'--sym-fc' parameter from "bte_command" of Phono3pyRun 
"""
if __name__ == '__main__': 
    root=os.getcwd()

    bsxs=["bs1","bs2","bs3","bs4","bs5","bs6","bs7","bs8"]

    rstfile=root+"/result/RMSEdata.csv"
    plotdir=root+"/result/grpplot/"
    colors=("black","red","pink","orange","yellow", "green","cyan","c","b")
    
    gdroot= "/home/okugawa/HDNNP/Si-190808"
    gdrstfile= gdroot+"/result/RMSEdata.csv"

    with open(rstfile, 'r') as rslt:
        readcsv = csv.reader(rslt)
        RMSEdata = []
        for row in readcsv:
            RMSEdata.append(float(row[1]))
            
    #Read RMSE data of "good sample"(d20n50)
    with open(gdrstfile, 'r') as grslt:
        readcsv = csv.reader(grslt)
        GRMSEdata = []
        for row in readcsv:
            if 'd20n50' in row[0]:
                GRMSEdata.append(float(row[1]))
            
    #Plotting all data of correlation of force/RMSE and TC error
    dtn=0
    allplotfile=plotdir+"alldata1-bs.png"
    fig = plt.figure()
    ax3 = fig.add_subplot(111)
    plt.title("All data (with '--sym-fc' parameter)")
    ax3.set_xlabel("TC Err (fm 112.1/300K)")
    ax3.set_ylabel("force/RMSE (meV/A)")
    ax3.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
            
    for i, bsx in enumerate(bsxs):
        for j in range(0, 10):
            TCfile= root+"/"+bsx+"-d20n50/"+str(j+1)+"/predict-phono3py/out.txt"
            with open(TCfile, 'r') as TCf:
                for n, line in enumerate(TCf):
                    if 'Thermal conductivity (W/m-k)' in line:
                        TCf.seek(0)
                        for lined in islice(TCf, n+32, n+33):
                            data=lined.split()
                            TCerr=abs(float(data[1])-112.1)
                
            ax3.scatter(TCerr,RMSEdata[dtn],c=colors[i+1],marker='.')
            dtn=dtn+1

    #Additional plot of "good sample"
    for j in range(0, 10):
        TCfile= gdroot+"/d20n50/"+str(j+1)+"/predict-phono3py/out.txt"
        with open(TCfile, 'r') as TCf:
            for n, line in enumerate(TCf):
                if 'Thermal conductivity (W/m-k)' in line:
                    TCf.seek(0)
                    for lined in islice(TCf, n+32, n+33):
                        data=lined.split()
                        TCerr=abs(float(data[1])-112.1)
                
            ax3.scatter(TCerr,GRMSEdata[j],c=colors[0],marker='.')

    left, right = ax3.get_xlim()
    ax3.set_xlim(-0.1, right*1.2)

    #ax4 is only for plotting legend of all kind of data
    ax4 = ax3.twinx()
    ax4.scatter(float(row[2]),float(row[1]),c=colors[0],marker='.',label="gs")
    for i, bsx in enumerate(bsxs):
        ax4.scatter(float(row[2]),float(row[1]),c=colors[i+1],marker='.',label=bsx)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax3.legend(handler4, label4,loc='upper right',title='Sample Grp',bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax4)
    plt.savefig(allplotfile)
    plt.close()
    