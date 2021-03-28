# -*- coding: utf-8 -*-
import re
import csv
import ast
from itertools import islice
import matplotlib.pyplot as plt

"""
This script is made to output csv file by gathering 
1) force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
2) train curve data (epoch, trained force/RMSE, validated, difference))
from RMSE/TC data of additional PCA-decompositted samples (dim=30 and no-PCA)
And plot train curve and scatter of force/RMSE&TC data
"""

if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/Si-190808"
    addgrps=["p30","noPCA"]
    grps=["p10","p15","p20","p30","noPCA"]
    colors=["red","orange","green","b","grey"]
    labels=["41->41","41->30","41->20","41->15","41->10","no PCA"]
    lcolors=["black","b","green","orange","red","grey"]

    rstfile=root+"/pca-result/RMSETCdata.csv"
    traindir=root+"/pca-result/traincv/"
    plotdir=root+"/pca-result/grpplot/"
    gdrstfile= root+"/result/RMSETCdata.csv"

    with open(rstfile, 'a') as rslt:
        writer1 = csv.writer(rslt, lineterminator='\n')
        
        for grp in addgrps:
            print(grp+" data gathering")

            for j in range(1, 11):
                dataname=grp+"-"+str(j)
                datadir= root+"/d20n50-"+grp+"/"+str(j)
                logfile= datadir+"/output/CrystalSi64/training.log"
                traincvfile= traindir+dataname+".csv"
                plotfile= traindir+"/plot/"+dataname+".png"

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
                    ax1.set_ylabel('force/RMSE (meV/A)')
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

    with open(gdrstfile,'r') as f1, open(rstfile,'r') as f2:
        RMSETC = []
        
        gsdt = csv.reader(f1)
        L1=0
        for row in gsdt:
            if 'd20n50-' in row[0]:
                RMSETC.append([float(row[1]),abs(float(row[2])),"black"])
                L1=L1+1

        pcadtcsv= csv.reader(f2)
        pcadt=list(pcadtcsv)
        L2=len(pcadt)
        for row in pcadt:
            gname = re.split('[-]',row[0])
            clr=colors[grps.index(gname[0])]
            RMSETC.append([float(row[1]),float(row[2]),clr])
                
    #Plotting force/RMSE and TC error of each sample
    allplotfile=plotdir+"alldata-pca.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("Result of PCA decomposition (data=700)")
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/A)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for RT in RMSETC:
        ax1.scatter(RT[1],RT[0],c=RT[2],marker='.')

    left, right = ax1.get_xlim()
    ax1.set_xlim(-0.1, right*1.2)

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for i, lbl in enumerate(labels):
        ax2.scatter(RT[1],RT[0],c=lcolors[i],marker='.',label=lbl)
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right',title='Feature Decomp',
               bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax2)
    plt.savefig(allplotfile)
    print(f'PCA decomposition chart is plotted: gs#={L1} decomp#={L2}')
    plt.close()