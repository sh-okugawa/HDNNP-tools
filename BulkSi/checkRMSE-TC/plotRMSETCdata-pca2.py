# -*- coding: utf-8 -*-
import re
import csv
import matplotlib.pyplot as plt

"""
This script is for plotting force/RMSE & TC err data of 
PCA-decompositted samples (dim=41(gs),30,20,15,10 and no-PCA)
"""

if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/Si-190808/"
    grps=["p10","p15","p20","p30","noPCA"]
    colors=["b","green","orange","lime","grey"]
    labels=["41=>41","41=>30","41=>20","41=>15","41=>10","no PCA"]
    lcolors=["red","lime","orange","green","b","grey"]

    rstfile=root+"result-pca/RMSETCdata.csv"
    gdrstfile= root+"result/RMSETCdata.csv"

    with open(gdrstfile,'r') as f1, open(rstfile,'r') as f2:
        RMSETC = []
        
        gsdt = csv.reader(f1)
        for row in gsdt:
            if 'd20n50-' in row[0]:
                RMSETC.append([float(row[1]),abs(float(row[2])),"red"])
        L1=len(RMSETC)

        pcadtcsv= csv.reader(f2)
        pcadt=list(pcadtcsv) 
        L2=len(pcadt)
        for row in pcadt:
            gname = re.split('[-]',row[0])
            clr=colors[grps.index(gname[0])]
            RMSETC.append([float(row[1]),abs(float(row[2])),clr])
                
    #Plotting force/RMSE and TC error of each sample
    allplotfile=root+"result-pca/grpplot/pca-all.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.xticks(fontsize=12)  #Font size of x-axis scale
    plt.yticks(fontsize=12)  #Font size of y-axis scale
    plt.title("Result of PCA decomposition (700 datas)",fontsize=14)
    ax1.set_xlabel("TC Err (from 112.1W/m-K:300K)",fontsize=12)
    ax1.set_ylabel("force/RMSE (meV/A)",fontsize=12)
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'  #Edge color of legend box
    plt.rcParams["legend.borderpad"] ='0.5'    #Space between handle & edge
    plt.rcParams["legend.handlelength"] ='1'   #Length of handle
    plt.rcParams["legend.handletextpad"] ='0.4' #Space between handle & label
    plt.rcParams["legend.labelspacing"] ='0.2' #Space between row of label
    for RT in RMSETC:
        ax1.scatter(RT[1],RT[0],c=RT[2],marker='.')

    left, right = ax1.get_xlim()
    ax1.set_xlim(-1, right*1.1)

    #ax2 is only for plotting legend of all kind of decomposition
    ax2 = ax1.twinx()
    for i, lbl in enumerate(labels):
        ax2.scatter(RT[1],RT[0],c=lcolors[i],marker='o',label=lbl)
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='lower right',fontsize=12,
              title='Decomp', title_fontsize=12)
    fig.delaxes(ax2)
    plt.savefig(allplotfile)
    print(f'PCA decomposition chart is plotted: gs#={L1} decomp#={L2}')
    plt.close()