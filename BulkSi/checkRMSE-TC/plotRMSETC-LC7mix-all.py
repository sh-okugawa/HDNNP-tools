# -*- coding: utf-8 -*-
import csv
import matplotlib.pyplot as plt

"""
This script is made to output csv file by gathering 3500smpl's
1) force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
2) train curve data (epoch, trained force/RMSE, validated, difference))
And plot train curve and scatter of force/RMSE&TC data
"""

if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/Si-200917/1000K-LC7/"
    smpls=["700smpl", "3500smpl"]

    rst3500smplfile=root+"result/3500smpl/RMSETCdata.csv"
    rst700smplfile=root+"result/700smpl/RMSETCdata.csv"
    orgresultdir= "/home/okugawa/HDNNP/Si-190808/result-LC7/"
    rstLinfile=root+"result/3500smpl-Lin/RMSETCdata.csv"
    rstSMZfile=root+"result/3500smpl-SMZ/RMSETCdata.csv"

    RMSETC=[]
    #Read force/RMSE & TC of 700smpl from csv
    with open(rst700smplfile,'r') as f1:
        gsdt = csv.reader(f1)
        L1,L2=0,0
        for row in gsdt:
            if 'mix-' in row[0]:
                if int(row[0].split('-')[1])<11:
                    RMSETC.append([float(row[1]),abs(float(row[2])),"blue"])
                    L1+=1
                else:
                    RMSETC.append([float(row[1]),abs(float(row[2])),"cyan"])
                    L2+=1
        print(f'force/RMSE & TC data of 700smpl ({L1}&{L2}) is read')

    #Read force/RMSE & TC of 3500smpl from csv
    with open(rst3500smplfile,'r') as f1:
        gsdt = csv.reader(f1)
        L1,L2=0,0
        for row in gsdt:
            if 'mix-' in row[0]:
                if int(row[0].split('-')[1])<11:
                    RMSETC.append([float(row[1]),abs(float(row[2])),"red"])
                    L1+=1
                else:
                    RMSETC.append([float(row[1]),abs(float(row[2])),"orange"])
                    L2+=1
        print(f'force/RMSE & TC data of 3500smpl ({L1}&{L2}) is read')
        
    #Read force/RMSE & TC of 3500smpl-Lin&SMZ from csv
    with open(rstSMZfile,'r') as f1, open(rstLinfile,'r') as f2:
        L1,L2=0,0
        gsdt = csv.reader(f1)
        for row in gsdt:
            if 'mix-' in row[0]:
                RMSETC.append([float(row[1]),abs(float(row[2])),"green"])
                L1+=1
        gsdt = csv.reader(f2)
        for row in gsdt:
            if 'mix-' in row[0]:
                RMSETC.append([float(row[1]),abs(float(row[2])),"lime"])
                L2+=1
        print(f'force/RMSE & TC data of 3500smpl-SMZ&Lin ({L1}&{L2}) is read')

    #Read force/RMSE & TC of original HDNNP's LC7mix 
    L1,L2=0,0
    for smpl in smpls:
        orgRMSETCfile=orgresultdir+smpl+"/RMSETCdata.csv"
        with open(orgRMSETCfile,'r') as f1:
            gsdt = csv.reader(f1)
            for row in gsdt:
                if 'mix-' in row[0]:
                    if smpl=="700smpl":
                        if row[0].split('-')[3]=="1":
                            RMSETC.append([float(row[1]),abs(float(row[2])),"black"])
                            L1+=1
                    else:
                        RMSETC.append([float(row[1]),abs(float(row[2])),"gray"])
                        L2+=1
                        
    print(f"Read force/RMSE & TC data of original HDNNP's LC7mix ({L1}&{L2})")

    #Plotting force/RMSE and TC error of each sample
    plotfile=root+"result/LC7mix-RMSETC-all.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("[Bulk-Si 1000K-LC7mix] TC err & force/RMSE")
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/ang)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for RT in RMSETC:
        ax1.scatter(RT[1],RT[0],c=RT[2],marker='.')

    #ax2 is only for plotting legend of data
    ax2 = ax1.twinx()
    ax2.scatter(0,0,c="green",marker='.',label="New-SMZsf (3500smpl,B=0.5)")
    ax2.scatter(0,0,c="lime",marker='.',label="New-Linsf (3500smpl,B=0.5)")
    ax2.scatter(0,0,c="blue",marker='.',label="New-NNP (700smpl,B=0.5)")
    ax2.scatter(0,0,c="cyan",marker='.',label="New-NNP (700smpl,B=0.99)")
    ax2.scatter(0,0,c="red",marker='.',label="New-NNP (3500smpl,B=0.5)")
    ax2.scatter(0,0,c="orange",marker='.',label="New-NNP (3500smpl,B=0.99)")
    ax2.scatter(0,0,c="black",marker='.',label="Orig-NNP (700smpl,B=0.99)")
    ax2.scatter(0,0,c="gray",marker='.',label="Orig-NNP (3500smpl,B=0.99)")
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2, bbox_to_anchor=(0.8, 0.95), loc='upper left')
    fig.delaxes(ax2)
    plt.savefig(plotfile,bbox_inches='tight')
    plt.close()
