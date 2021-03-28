# -*- coding: utf-8 -*-
import csv,sys
import re
import matplotlib.pyplot as plt

"""
This script is for plotting scatter of force/RMSE&TC data from
 each RMSETCdata.csv
"""

if __name__ == '__main__':
    T5L7folder="/home/okugawa/HDNNP/Si-200917/T5L7/"
    T5L7data= T5L7folder+"result/RMSETCdata.csv"
    smalldata="/home/okugawa/HDNNP/Si-200917/small/result/RMSETCdata.csv"
    grps= ["TH3-L7","TH3-L79","TH3-LM3","TM3-L7","TM3-L79","TM3-LM3",
           "TL3-L7","TL3-L79","TL3-LM3","all60"]

    plotfile=T5L7folder+"result/RMSETC-T5L7.png"
    colors=["b","b","cyan","green","green","lime","red","red","orange",
            "brown","grey"]
    marks=["+",".",".","+",".",".","+",".",".","+","+"]
    lbls=["T:H3-L:7(2100)","T:H3-L:7(900)","T:H3-L:3(900)",
          "T:M3-L:7(2100)","T:M3-L:7(900)","T:M3-L:3(900)",
          "T:L3-L:7(2100)","T:L3-L:7(900)","T:L3-L:3(900)",
          "T:5-L:7(2100)","small(2100)"]
    
    #Plotting force/RMSE and TC error of each sample
    with open(T5L7data,'r') as f1, open(smalldata,'r') as f2:
        RMSETC = []
        T5L7dt = csv.reader(f1)
        for row in T5L7dt:
            dname = re.split('[-]',row[0])
            if len(dname)==3:
                dataname = dname[0]+"-"+dname[1]
            elif len(dname)==2:
                dataname = dname[0]
            else:
                print(f'Data name length error: {len(dname)}')
                sys.exit()
            grpindex= grps.index(dataname)
            RMSETC.append([float(row[1]),abs(float(row[2])),colors[grpindex],
                           marks[grpindex]])

        sm0599= csv.reader(f2)
        for row in sm0599:
            if 'small-' in row[0]:
                dname = re.split('[-]',row[0])
                if int(dname[1])>30:
                    RMSETC.append([float(row[1]),abs(float(row[2])),"grey","+"])
                   
    #Plotting force/RMSE and TC error of each sample
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("force/RMSE & TC of each sample (Temp:5 LC:7)")
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/ang)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    plt.rcParams["legend.borderpad"] ='0.3'    #Space between handle & edge
    plt.rcParams["legend.handlelength"] ='1'   #Length of handle
    plt.rcParams["legend.handletextpad"] ='0.2' #Space between handle & label
    plt.rcParams["legend.columnspacing"] ='1'  #Space between columns
    plt.rcParams["legend.labelspacing"] ='0.2' #Space between row of label

    for RTdata in RMSETC:
        ax1.scatter(RTdata[1],RTdata[0],c=RTdata[2],marker=RTdata[3])

    left, right = ax1.get_xlim()
    ax1.set_xlim(left, right*1.4)

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(11):
        ax2.scatter(RTdata[1],RTdata[0],c=colors[k],marker=marks[k],label=lbls[k])
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right')
    fig.delaxes(ax2)
    plt.savefig(plotfile)
    plt.close()