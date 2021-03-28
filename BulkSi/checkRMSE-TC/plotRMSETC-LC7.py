# -*- coding: utf-8 -*-
import csv
import re
import sys
import matplotlib.pyplot as plt

"""
This script is made to output csv file by gathering 
1) force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
2) train curve data (epoch, trained force/RMSE, validated, difference))
from RMSE/TC data of MD-LC7 samples (700samples from 5000samples of 1000K-LCx7)
And plot train curve and scatter of force/RMSE&TC data
"""

def plotLC7RMSETC(rstfile,plotfile1,title1,plotfile2,title2):
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05']
    colors=["purple","orange","pink","lime","cyan","deepskyblue","b","red","gray","black"]
    gdrstfile= "/home/okugawa/HDNNP/Si-190808/result/RMSETCdata.csv"
    
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
                clr=colors[grps.index(gname[1])]
                RMSETC.append([float(row[1]),abs(float(row[2])),clr])
                L2=L2+1
            elif gname[1]=="mix":
                if gname[3]=="1":
                    RMSETC.append([float(row[1]),abs(float(row[2])),"red"])
                    L2=L2+1
            else:
                print(f'Error: Grpname [{gname[1]}] is not valid.')
                sys.exit()
                
    #Plotting force/RMSE and TC error of each sample

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title(title1)
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
    print(f'[{title1}] LC7({L2}) & gs({L1}) are plotted')
    plt.close()
    
    #Plotting force/RMSE and TC error of all mix data
    with open(rstfile,'r') as f1:
        RMSETC = []
        mddt1= csv.reader(f1)
        L3=0
        for row in mddt1:
            gname = re.split('[-]',row[0])
            if gname[1]=="mix":
                clr=colors[int(gname[2])-1]
                RMSETC.append([float(row[1]),abs(float(row[2])),clr])
                L3=L3+1
                
    #Plotting force/RMSE and TC error of each sample
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title(title2)
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
    print(f'[{title2}] LC7 all of mix({L3}) are plotted')
    plt.close()
    
if __name__ == '__main__':
    lmpfolder="/home/okugawa/HDNNP/Si-190808/"
    rstfile=lmpfolder+"result-LC7/RMSETCdata.csv"
    plotfile1=lmpfolder+"result-LC7/grpplot/alldata-lmp-LC7.png"
    title1="Lammps-MD 1000K-LC7 & LCmix & gs"
    plotfile2=lmpfolder+"result-LC7/grpplot/allmix-lmp-LC7n.png"
    title2="Lammps-MD 1000K-LC7-mix-all"
    plotLC7RMSETC(rstfile,plotfile1,title1,plotfile2,title2)

    mdfolder="/home/okugawa/HDNNP/Si-190808-md/"
    rstfile=mdfolder+"result-LC7/RMSETCdata.csv"
    plotfile1=mdfolder+"result-LC7/grpplot/alldata-md-LC7.png"
    title1="AIMD 1000K-LC7 & LCmix & gs"
    plotfile2=mdfolder+"result-LC7/grpplot/allmix-md-LC7.png"
    title2="AIMD 1000K-LC7-mix-all"
    plotLC7RMSETC(rstfile,plotfile1,title1,plotfile2,title2)
    
    rstfile=mdfolder+"result-LC7n/RMSETCdata.csv"
    plotfile1=mdfolder+"result-LC7n/grpplot/alldata-md-LC7n.png"
    title1="AIMD 1000K-LC7n & LCmix & gs"
    plotfile2=mdfolder+"result-LC7n/grpplot/allmix-md-LC7n.png"
    title2="AIMD 1000K-LC7n-mix-all"
    plotLC7RMSETC(rstfile,plotfile1,title1,plotfile2,title2)