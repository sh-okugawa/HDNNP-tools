# -*- coding: utf-8 -*-
import csv
import matplotlib.pyplot as plt

"""
This script is plotting scatter of force/RMSE&TC data of 
MD 1000K/1200K, 1000K-LCx3 and gs
"""

if __name__ == '__main__': 
    mdfolder="/home/okugawa/HDNNP/Si-190808-md"
    grps=['gs','1000K0.99','1000K1.0','1000K1.01','1000K','1200K']

    rstfile1=mdfolder+"/result-LC/RMSETCdata.csv"
    rstfile2=mdfolder+"/result/RMSETCdata.csv"
    gdrstfile= "/home/okugawa/HDNNP/Si-190808/result/RMSETCdata.csv"
    plotdir=mdfolder+"/result-LC/grpplot/"
    colors=("black","blue","cyan","green","orange","red")

    with open(gdrstfile,'r') as f1, open(rstfile1,'r') as f2, open(rstfile2,'r') as f3:
        RMSETC = []
        
        gsdt = csv.reader(f1)
        L1=0
        for row in gsdt:
            if 'd20n50-' in row[0]:
                RMSETC.append([float(row[1]),float(row[2])])
                L1=L1+1
        mddt1= csv.reader(f2)
        L2=0
        for row in mddt1:
            RMSETC.append([float(row[1]),float(row[2])])
            L2=L2+1
        mddt2= csv.reader(f3)
        L3=0
        for row in mddt2:
            RMSETC.append([float(row[1]),float(row[2])])
            L3=L3+1
                
    #Plotting force/RMSE and TC error of each sample
    allplotfile=plotdir+"alldata-na-md.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("All data of MD 1000K-LCx3 & 1000K/1200K & gs")
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/A)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for k in range(6):
        for j in range(10):
            num=k*10+j
            ax1.scatter(RMSETC[num][1],RMSETC[num][0],c=colors[k],marker='.')

#    left, right = ax1.get_xlim()
#    ax1.set_xlim( left, right*1.3)

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(6):
        ax2.scatter(float(row[2]),float(row[1]),c=colors[k],marker='.',label=grps[k])
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='lower left',title='Sample Grp',
               bbox_to_anchor=(0,0),borderaxespad=0.5)
    fig.delaxes(ax2)
    plt.savefig(allplotfile)
    print(f'Scatter of MD1000K-LCx3({L2}) & MD1000K/1200K({L3}) & gs({L1}) are plotted')
    plt.close()