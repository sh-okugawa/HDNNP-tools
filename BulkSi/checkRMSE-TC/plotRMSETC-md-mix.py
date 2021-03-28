# -*- coding: utf-8 -*-
import csv
import ast
import re
from itertools import islice
import matplotlib.pyplot as plt

"""
This script is made to output csv file by gathering 
1) force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
2) train curve data (epoch, trained force/RMSE, validated, difference))
from RMSE/TC data of MD samples (700samples from 5000samples of 1000K-LCx4)
And plot train curve and scatter of force/RMSE&TC data
"""

if __name__ == '__main__': 
    mdfolder="/home/okugawa/HDNNP/Si-190808-md"
    grps=['gs','1000K0.99','1000K1.0','1000K1.01','1000Kmix','1000K','1200K']

    rstfile1=mdfolder+"/result-LC/RMSETCdata.csv"
    rstfile2=mdfolder+"/result/RMSETCdata.csv"
    gdrstfile= "/home/okugawa/HDNNP/Si-190808/result/RMSETCdata.csv"
    plotdir=mdfolder+"/result-LC/grpplot/"
    colors=("black","blue","cyan","green","red","orange","pink")

    grp='1000Kmix'
    traindir=mdfolder+"/result-LC/traincv/"

    with open(gdrstfile,'r') as f1, open(rstfile1,'r') as f2, open(rstfile2,'r') as f3:
        RMSETC = []
        gsdt = csv.reader(f1)
        L1=0
        for row in gsdt:
            if 'd20n50-' in row[0]:
                RMSETC.append([float(row[1]),abs(float(row[2])),colors[0]])
                L1=L1+1
        mddt1= csv.reader(f2)
        L2=0
        for row in mddt1:
            gname = re.split('[-]',row[0])
            clr=colors[grps.index(gname[0])]
            RMSETC.append([float(row[1]),abs(float(row[2])),clr])
            L2=L2+1
        mddt2= csv.reader(f3)
        L3=0
        for row in mddt2:
            gname = re.split('[-]',row[0])
            clr=colors[grps.index(gname[0])]
            RMSETC.append([float(row[1]),abs(float(row[2])),clr])
            L3=L3+1
                
    #Plotting force/RMSE and TC error of each sample
    allplotfile=plotdir+"alldata-md-LC.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("MD 1000K-LC(0.99,1.0,1.01,mix) & 1000K/1200K & gs")
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
    for k in range(7):
        ax2.scatter(RTdata[1],RTdata[0],c=colors[k],marker='.',label=grps[k])
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right',title='Sample Grp',
               bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax2)
    plt.savefig(allplotfile)
    print(f'Scatter of MD1000K-LCx4({L2}) & MD1000K/1200K({L3}) & gs({L1}) are plotted')
    plt.close()