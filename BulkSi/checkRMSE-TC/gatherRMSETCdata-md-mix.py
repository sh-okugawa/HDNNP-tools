# -*- coding: utf-8 -*-
import csv
import ast
import re
from itertools import islice
import matplotlib.pyplot as plt

"""
This script is made to output csv file by gathering 
1) force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
2) train curve data (epoch, trained force/RMSE, validated, difference))
from RMSE/TC data of MD samples (700samples from 5000samples of 1000K-LCx4)
And plot train curve and scatter of force/RMSE&TC data
"""

if __name__ == '__main__': 
    mdfolder="/home/okugawa/HDNNP/Si-190808-md"
    grps=['gs','1000K0.99','1000K1.0','1000K1.01','1000Kmix','1000K','1200K']

    rstfile1=mdfolder+"/result-LC/RMSETCdata.csv"
    rstfile2=mdfolder+"/result/RMSETCdata.csv"
    gdrstfile= "/home/okugawa/HDNNP/Si-190808/result/RMSETCdata.csv"
    plotdir=mdfolder+"/result-LC/grpplot/"
    colors=("black","blue","cyan","green","red","orange","pink")

    grp='1000Kmix'
    traindir=mdfolder+"/result-LC/traincv/"
    
    #Adding RMSE and TC of 1000Kmix to RMSETCdata.csv and Plotting training curve
    with open(rstfile1, 'a') as rslt:
        writer1 = csv.writer(rslt, lineterminator='\n')
        print(grp+" data gathering")

        for j in range(1, 11):
            dataname=grp+"-"+str(j)
            datadir= mdfolder+"/"+grp+"/"+str(j)
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
                            TCerr=float(data[1])-112.1

            RMSETCdt=[dataname]+[vf]+[TCerr]
            writer1.writerow(RMSETCdt)
            
    #Plotting force/RMSE and TC error of each sample
    with open(gdrstfile,'r') as f1, open(rstfile1,'r') as f2, open(rstfile2,'r') as f3:
        RMSETC = []
        gsdt = csv.reader(f1)
        L1=0
        for row in gsdt:
            if 'd20n50-' in row[0]:
                RMSETC.append([float(row[1]),abs(float(row[2])),colors[0]])
                L1=L1+1
        mddt1= csv.reader(f2)
        L2=0
        for row in mddt1:
            gname = re.split('[-]',row[0])
            clr=colors[grps.index(gname[0])]
            RMSETC.append([float(row[1]),abs(float(row[2])),clr])
            L2=L2+1
        mddt2= csv.reader(f3)
        L3=0
        for row in mddt2:
            gname = re.split('[-]',row[0])
            clr=colors[grps.index(gname[0])]
            RMSETC.append([float(row[1]),abs(float(row[2])),clr])
            L3=L3+1
                
    #Plotting force/RMSE and TC error of each sample
    allplotfile=plotdir+"alldata-md-LC.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("MD 1000K-LC(0.99,1.0,1.01,mix) & 1000K/1200K & gs")
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/A)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for RTdata in RMSETC:
        ax1.scatter(RTdata[1],RTdata[0],c=RTdata[2],marker='.')

    left, right = ax1.get_xlim()
    ax1.set_xlim(-0.1, right*1.2)

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(7):
        ax2.scatter(RTdata[1],RTdata[0],c=colors[k],marker='.',label=grps[k])
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right',title='Sample Grp',
               bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax2)
    plt.savefig(allplotfile)
    print(f'Scatter of MD1000K-LCx4({L2}) & MD1000K/1200K({L3}) & gs({L1}) are plotted')
    plt.close()