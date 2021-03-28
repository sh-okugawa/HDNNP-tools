# -*- coding: utf-8 -*-
import sys
import csv
import re
from itertools import islice
import matplotlib.pyplot as plt

"""
This script is plotting good sample and all of bad sample data with 
removing '--sym-fc' parameter from "bte_command" of Phono3pyRun 
"""

def gatherTC(TCdir):
    TCfile= TCdir+"/predict-phono3py2/out.txt"
    with open(TCfile, 'r') as TCf:
        for n, line in enumerate(TCf):
            if 'Thermal conductivity (W/m-k)' in line:
                TCf.seek(0)
                for lined in islice(TCf, n+32, n+33):
                    data=lined.split()
                    TCerr=abs(float(data[1])-112.1)
    return(TCerr)
   
if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/Si-190808/"
    rstfile=root+"/result-LC7/RMSETCdata.csv"
    plotdir=root+"/result-LC7/grpplot/"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05']
    colors=["purple","orange","pink","lime","cyan","deepskyblue","b","red","gray","black"]
    gdrstfile= root+"/result/RMSETCdata.csv"
        
    #Plotting force/RMSE and TC error of each sample
    with open(gdrstfile,'r') as f1, open(rstfile,'r') as f2:
        RMSETC = []
        gsdt = csv.reader(f1)
        L1=0
        for row in gsdt:
            if 'd20n50-' in row[0]:
                RMSETC.append([float(row[1]),abs(float(row[2])),"black"])
                L1=L1+1

        mddt1= csv.reader(f2)
        L2=0
        for row in mddt1:
            gname = re.split('[-]',row[0])
            if gname[1] in grps:
                TCdir=root+"1000K-LC7/"+gname[1]+"/"+gname[2]
                TCerr=gatherTC(TCdir)
                clr=colors[grps.index(gname[1])]
                RMSETC.append([float(row[1]),TCerr,clr])
                L2=L2+1
            elif gname[1]=="mix":
                if gname[3]=="1":
                    TCdir=root+"1000K-LC7/mix/"+gname[2]+"/1"
                    TCerr=gatherTC(TCdir)
                    RMSETC.append([float(row[1]),TCerr,"red"])
                    L2=L2+1
            else:
                print(f'Error: Grpname [{gname[1]}] is not valid.')
                sys.exit()
                
    #Plotting force/RMSE and TC error of each sample
    plotfile1 = plotdir+"alldata-lmp-LC7-noSF.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("Lammps-MD LC7 force/RMSE & TC(w/o '--sym-fc')")
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/A)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for RTdata in RMSETC:
        ax1.scatter(RTdata[1],RTdata[0],c=RTdata[2],marker='.')

    left, right = ax1.get_xlim()
    ax1.set_xlim(-0.1, right*1.2)

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    ax2.scatter(RTdata[1],RTdata[0],c="black",marker='.',label="gs")
    for k in range(7):
        lbl="LC="+grps[k]
        ax2.scatter(RTdata[1],RTdata[0],c=colors[k],marker='.',label=lbl)
    ax2.scatter(RTdata[1],RTdata[0],c="red",marker='.',label="LCmix")
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right',title='Sample Grp',
               bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax2)
    plt.savefig(plotfile1)
    print(f'[1000K-LC7 w/o --sym-fc] LC7({L2}) & gs({L1}) are plotted')
    plt.close()
    
    #Plotting force/RMSE and TC error of all mix data
    plotfile2 = plotdir+"allmix-lmp-LC7-noSF.png"
    with open(rstfile,'r') as f1:
        RMSETC = []
        mddt1= csv.reader(f1)
        L3=0
        for row in mddt1:
            gname = re.split('[-]',row[0])
            if gname[1]=="mix":
                TCdir=root+"1000K-LC7/mix/"+gname[2]+"/"+gname[3]
                TCerr=gatherTC(TCdir)
                clr=colors[int(gname[2])-1]
                RMSETC.append([float(row[1]),TCerr,clr])
                L3=L3+1
                
    #Plotting force/RMSE and TC error of each sample
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("Lammps-MD LC7mix force/RMSE & TC(w/o '--sym-fc')")
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/A)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for RTdata in RMSETC:
        ax1.scatter(RTdata[1],RTdata[0],c=RTdata[2],marker='.')

    left, right = ax1.get_xlim()
    ax1.set_xlim(-0.1, right*1.2)

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(10):
        lbl="LC7xyz-"+str(k+1)
        ax2.scatter(RTdata[1],RTdata[0],c=colors[k],marker='.',label=lbl)
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right',title='Sample Grp',
               bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax2)
    plt.savefig(plotfile2)
    print(f'[1000K-LC7 w/o --sym-fc] all of mix({L3}) are plotted')
    plt.close()