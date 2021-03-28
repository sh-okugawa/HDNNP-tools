# -*- coding: utf-8 -*-
import csv
import ast
from itertools import islice
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

    with open(rstfile, 'w') as rslt:
        writer1 = csv.writer(rslt, lineterminator='\n')
        RMSETC = []
        
        for grp in grps:
            for j in range(1, 21):
                dataname=grp+"-"+str(j)
                datadir= root+grp+"/"+str(j)
                logfile= datadir+"/output/CrystalSi64/training.log"
                traincvfile= traindir+dataname+".csv"
                plotfile= traindir+"plot/"+dataname+".png"
                clr="blue"
                
                if j>10:
                    clr="red"

                with open(logfile, 'r') as log:
                    logdata= log.read()
                    listdata= ast.literal_eval(logdata)
                    listlen= len(listdata)
                    diffnum=0
                    difftotal=0
                    epl=[]
                    tfl=[]
                    vfl=[]
                    diffl=[]
                    with open(traincvfile, 'w') as tcv:
                        writer2 = csv.writer(tcv, lineterminator='\n')
                        for epc in range(9, listlen, 10):
                            ep=int(listdata[epc]["epoch"])
                            tf=float(listdata[epc]["main/RMSE/force"])*1000
                            vf=float(listdata[epc]["val/main/RMSE/force"])*1000
                            diff=vf-tf
                            outdata=[ep]+[tf]+[vf]+[diff]
                            writer2.writerow(outdata)
                            epl.append(ep)
                            tfl.append(tf)
                            vfl.append(vf)
                            diffl.append(diff)
                                
                    # Plotting Training curve and diff of Train&Validation
                    # Axis-1: ax1 for Train and Validation
                    # Axis-2: ax2 for difference of Train and Validation
                    fig = plt.figure()
                    ax1 = fig.add_subplot(111)
                    ln1 = ax1.plot(epl, tfl, color="blue", label="Train")
                    ln2 = ax1.plot(epl, vfl, color="red", label="Validation")
                    ax2 = ax1.twinx()  # convining ax1 and ax2
                    ln3 = ax2.plot(epl, diffl, color="green", label="Diff")
                    ax2.set_ylim(-28, 22)  # fixing y-axis scale 
                    plt.title(dataname)
                    ax1.set_xlabel('epoch')
                    ax1.set_ylabel('force/RMSE (meV/ang)')
                    ax1.grid(True)
                    ax2.set_ylabel('Diff (Val-Trn)')
                    # merging legend of ax1 and ax2
                    handler1, label1 = ax1.get_legend_handles_labels()
                    handler2, label2 = ax2.get_legend_handles_labels()
                    ax1.legend(handler1 + handler2, label1 + label2, loc=2)
                    plt.savefig(plotfile)
                    plt.close()
                    
                TCfile =datadir+"/predict-phono3py/out.txt"
                with open(TCfile, 'r') as TCf:
                    for n, line in enumerate(TCf):
                        if 'Thermal conductivity (W/m-k)' in line:
                            TCf.seek(0)
                            for lined in islice(TCf, n+32, n+33):
                                data=lined.split()
                                TCerr=abs(float(data[1])-112.1)

                RMSETCdt=[dataname]+[vf]+[TCerr]
                writer1.writerow(RMSETCdt)
                RMSETC.append([vf,TCerr,clr])
                print(f'{dataname} data is gathered and train curve is plotted')

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