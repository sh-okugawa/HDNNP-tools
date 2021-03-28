# -*- coding: utf-8 -*-
import csv
import re
import matplotlib.pyplot as plt

"""
This script is for plotting scatter of force/RMSE&TC data from
 each RMSETCdata.csv
"""

if __name__ == '__main__':
    rootnew="/home/okugawa/test-HDNNP-new/HDNNP/Si-200917/"
    LC7mdata=rootnew+"1000K-LC7/mix/3500smpl/result/RMSETCdata.csv"
    LC3mdata=rootnew+"1000K-LC3/mix/3000smpl/result/RMSETCdata.csv"
    LC1data=rootnew+"1000K-LC1/1500smpl/result/RMSETCdata.csv"
    TMP5LC7data="/home/okugawa/HDNNP/Si-190808/result/RMSETCdata-TMP5LC7.csv"
    smalldata=rootnew+"small/result/RMSETCdata.csv"
    plotfile=rootnew+"small/result/RMSETC-LC7LC3LC1small.png"
    colors=["orange","red","b","green","cyan","brown","darkgray"]
    lbls=["small-0.5","small-0.99","LC7m-0.5","LC7m-0.99","LC3m-0.99","LC1-0.99","T5L7-0.99"]
    
    #Plotting force/RMSE and TC error of each sample
    with open(LC7mdata,'r') as f1, open(smalldata,'r') as f2:
        RMSETC = []
        L0599 = csv.reader(f1)
        L1, L2 = 0,0
        for row in L0599:
            if 'LC7mix-3500' in row[0]:
                dname = re.split('[-]',row[0])
                if int(dname[2])>10:
                    RMSETC.append([float(row[1]),abs(float(row[2])),"b"])
                    L1+=1
                else:
                    RMSETC.append([float(row[1]),abs(float(row[2])),"green"])
                    L2+=1

        sm0599= csv.reader(f2)
        L3, L4 = 0,0
        for row in sm0599:
            if 'small-' in row[0]:
                dname = re.split('[-]',row[0])
                if int(dname[1])<11:
                    RMSETC.append([float(row[1]),abs(float(row[2])),"orange"])
                    L3+=1
                else:
                    RMSETC.append([float(row[1]),abs(float(row[2])),"red"])
                    L4+=1

    with open(LC3mdata,'r') as f3, open(LC1data,'r') as f4:
        LC3dt = csv.reader(f3)
        LC1dt = csv.reader(f4)
        L5, L6 = 0,0
        for row in LC3dt:
            if 'LC3mix-3000' in row[0]:
                RMSETC.append([float(row[1]),abs(float(row[2])),"cyan"])
                L5+=1

        for row in LC1dt:
            if 'LC1.00-1500' in row[0]:
                RMSETC.append([float(row[1]),abs(float(row[2])),"brown"])
                L6+=1

    with open(TMP5LC7data,'r') as f5:
        T5L7dt = csv.reader(f5)
        L7 = 0
        for row in T5L7dt:
            if 'd100n200-' in row[0]:
                RMSETC.append([float(row[1]),abs(float(row[2])),"darkgray"])
                L7+=1

                    
    #Plotting force/RMSE and TC error of each sample
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("1000K-LC7mix & LC3mix & LC1.00 & small")
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/ang)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for RTdata in RMSETC:
        ax1.scatter(RTdata[1],RTdata[0],c=RTdata[2],marker='.')

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(7):
        ax2.scatter(RTdata[1],RTdata[0],c=colors[k],marker='.',label=lbls[k])
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right')
    fig.delaxes(ax2)
    plt.savefig(plotfile)
    print(f'Scatter of LC7-05({L1}),LC7-099({L2}),LC3-099({L5}),LC1-099({L6}) &')
    print(f' small-05({L3}),small-099({L4}),TMP5LC7-099({L7}) are plotted')
    plt.close()