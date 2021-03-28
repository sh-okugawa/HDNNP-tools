# -*- coding: utf-8 -*-
import ast
import csv
import re
import matplotlib.pyplot as plt

"""
This script is for plotting force/RMSE of Rs=0 of previous LC7mix data
"""
            
if __name__ == '__main__':
    root="/home/okugawa/HDNNP/Si-190808/"
    Rsfolder=root+"1000K-LC7/Rs/mix/"
    lbl=['Rs=0(G2:3)','Rs=0(G2:10)','Rs=0(G2:24)','Rs:Org(G2:24)']
    colors=["red","b","green","black"]
    xlb=[str(i+1) for i in range(10)]
    
    plotfile=root+"result-LC7/Rs/Rs.png"
    gdrstfile= root+"result-LC7/RMSETCdata.csv"
    
    #Read force/RMSE data from log file
    vfl=[[] for n in range(4)]

    #Plotting force/RMSE and TC error of each sample
    with open(gdrstfile,'r') as f1:
        gsdt = csv.reader(f1)
        for row in gsdt:
            if '1000KLC7-mix-' in row[0]:
                gname = re.split('[-]',row[0])
                if gname[3]=='1':
                    vfl[3].append(float(row[1]))
    
    for i in range(3):
        for j in range(1, 11):
            logfile=Rsfolder+str(i+1)+"/"+str(j)+"/output/CrystalSi64/training.log"
            with open(logfile, 'r') as log:
                logdata= log.read()
                listdata= ast.literal_eval(logdata)
                vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                vfl[i].append(vf)

    #Plotting force/RMSE of each Rc & Hidden-layer#
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("force/RMSE of 1000K-LC7mix (Rs=0)")
    ax1.set_xlabel("mix xyz-data#")
    ax1.set_ylabel("force/RMSE (meV/A)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for nn,vfdt in enumerate(vfl):
        clr=colors[nn]
        ax1.scatter(xlb,vfdt,c=clr,marker='o')

    left, right = ax1.get_xlim()
    ax1.set_xlim(-0.1, right*1.5)

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(4):
        ax2.scatter(xlb,vfdt,c=colors[k],marker='o',label=lbl[k])
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right',title='Rs modify')
    fig.delaxes(ax2)
    plt.savefig(plotfile)
    print(f'force/RMSE of each Rs parms are plotted. gs#={len(vfl[3])}')
    plt.close()