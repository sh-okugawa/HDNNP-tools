# -*- coding: utf-8 -*-
import csv
import matplotlib.pyplot as plt

"""
This script is made to output csv file by gathering 
1) force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
2) train curve data (epoch, trained force/RMSE, validated, difference))
And plot train curve and scatter of force/RMSE&TC data
"""

if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/Si-200917/1000K-LC7/"
    grps=["mix"]

    rstfile=root+"result/RMSETCdata.csv"
    traindir=root+"result/traincv/"
    plotdir=root+"result/grpplot/"
    orgRMSETCfile= "/home/okugawa/HDNNP/Si-190808/result-LC7/RMSETCdata.csv"

    RMSETC = []
    with open(rstfile, 'r') as rslt:
        RTdata = csv.reader(rslt)
        for row in RTdata:
            if "mix-" in row[0]:
                if int(row[0].split('-')[1]) < 11:
                    clr="blue"
                else:
                    clr="red"
                RMSETC.append([float(row[1]),abs(float(row[2])),clr])
        
    #Read force/RMSE & TC of original HDNNP's LC7mix 
    with open(orgRMSETCfile,'r') as f1:
        gsdt = csv.reader(f1)
        L1=0
        for row in gsdt:
            if '1000KLC7-mix-' in row[0]:
                if row[0].split('-')[3]=="1":
                    RMSETC.append([float(row[1]),abs(float(row[2])),"black"])
                    L1=L1+1
    print(f"Read force/RMSE & TC data of original HDNNP's LC7mix ({L1})")

    #Plotting force/RMSE and TC error of each sample
    plotfile=plotdir+"LC7mix-RMSETC.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("[Bulk-Si 1000K-LC7mix] TC err & force/RMSE by revised HDNNP")
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/ang)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for RT in RMSETC:
        ax1.scatter(RT[1],RT[0],c=RT[2],marker='.')
    left, right = ax1.get_xlim()
    ax1.set_xlim(-0.1, right*1.2)

    #ax2 is only for plotting legend of data
    ax2 = ax1.twinx()
    ax2.scatter(RT[1],RT[0],c="blue",marker='.',label="New HDNNP (mixB=0.5)")
    ax2.scatter(RT[1],RT[0],c="red",marker='.',label="New HDNNP (mixB=0.99)")
    ax2.scatter(RT[1],RT[0],c="black",marker='.',label="Orig HDNNP (mixB=0.99)")
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2, loc='center right')
    fig.delaxes(ax2)
    plt.savefig(plotfile)
    plt.close()