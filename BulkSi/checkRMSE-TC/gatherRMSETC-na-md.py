# -*- coding: utf-8 -*-
import csv
import ast
from itertools import islice
import matplotlib.pyplot as plt

"""
This script is made to output csv file by gathering 
force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
from RMSE/TC data of MD samples (700samples from 5000samples of 1000K/1200K)
And plot scatter of force/RMSE&TC data
"""

if __name__ == '__main__': 
    mdfolder="/home/okugawa/HDNNP/Si-190808-md"
    grps=['1000K','1200K']

    rstfile=mdfolder+"/result/RMSETCdata.csv"
    plotdir=mdfolder+"/result/grpplot/"
    gdroot= "/home/okugawa/HDNNP/Si-190808"
    gdrstfile= gdroot+"/result/RMSETCdata.csv"
    colors=("black","red","b")

    with open(rstfile, 'w') as rslt:
        writer1 = csv.writer(rslt, lineterminator='\n')
        RMSETC = []
        
        for grpnum,grp in enumerate(grps):
            print(grp+" data gathering")

            for j in range(1, 11):
                dataname=grp+"-"+str(j)
                datadir= mdfolder+"/"+grp+"/"+str(j)
                logfile= datadir+"/output/CrystalSi64/training.log"

                with open(logfile, 'r') as log:
                    logdata= log.read()
                    listdata= ast.literal_eval(logdata)
                    listlen= len(listdata)
                    for epc in range(9, listlen, 10):
                        vf=float(listdata[epc]["val/main/RMSE/force"])*1000
                    
                TCfile =datadir+"/predict-phono3py/out.txt"
                with open(TCfile, 'r') as TCf:
                    for n, line in enumerate(TCf):
                        if 'Thermal conductivity (W/m-k)' in line:
                            TCf.seek(0)
                            for lined in islice(TCf, n+32, n+33):
                                data=lined.split()
                                TCerr=float(data[1])-112.1

                RMSETCdt=[dataname]+[vf]+[TCerr]
                writer1.writerow(RMSETCdt)
                RMSETC.append([vf,TCerr])
                
    #Plotting force/RMSE and TC error of each sample
    allplotfile=plotdir+"1000K1200Kdata-md.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("All data of MD 1000K/1200K")
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/A)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for grpnum,grp in enumerate(grps):
        for j in range(1, 11):
            num=grpnum*10+j-1
            ax1.scatter(RMSETC[num][1],RMSETC[num][0],c=colors[grpnum+1],marker='.')

    #Read RMSE data of "good sample"(d20n50)
    with open(gdrstfile, 'r') as grslt:
        GRMSETC = []
        gsdt = csv.reader(grslt)
        L1=0
        for row in gsdt:
            if 'd20n50-' in row[0]:
                GRMSETC.append([float(row[1]),float(row[2])])
                L1=L1+1

    #Additional plot of "good sample"
    for GRMSETCdata in GRMSETC:
        ax1.scatter(GRMSETCdata[1],GRMSETCdata[0],c=colors[0],marker='.')

    left, right = ax1.get_xlim()
    ax1.set_xlim(left, right*1.2)

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    ax2.scatter(float(row[2]),float(row[1]),c=colors[0],marker='.',label="gs")
    for i, grp in enumerate(grps):
        ax2.scatter(float(row[2]),float(row[1]),c=colors[i+1],marker='.',label=grp)
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right',title='Sample Grp',
               bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax2)
    plt.savefig(allplotfile)
    plt.close()