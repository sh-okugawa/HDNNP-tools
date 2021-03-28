# -*- coding: utf-8 -*-
import ast
import matplotlib.pyplot as plt

"""
This script is for plotting force/RMSE of Amorphous-Si samples
"""
            
if __name__ == '__main__':
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    grps=['300','315','500-10','500-30','500-40','1000-10','1000-30','1000-40',
          '1000-103040','1500-103040']
    colors=["red","orange","hotpink","brown","green","lime","b","deepskyblue",
            "olive","cyan","purple"]
    lbls=["300smpl","315smpl (r_mq:mix)",
           "500smpl (r_mq=1000)","500smpl (r_mq=5000)","500smpl (r_mq=10000)",
           "1000smpl (r_mq=1000)","1000smpl (r_mq=5000)","1000smpl (r_mq=10000)",
           "1000smpl (r_mq:mix)","1500smpl (r_mq:mix)","1500smpl (r_mq:mix) n40"]
    
    plotfile=amrfolder+"result/amrSi-fRMSE-all4.png"
    logf="/output/AmorphousSi216/training.log"
    
    #Read force/RMSE data from log file
    vfl=[[],[],[]]
    for gn,grp in enumerate(grps):
        if grp=="300":
            logfolder=amrfolder+"amr216/"+grp+"smpl/40-3/"
        else:
            logfolder=amrfolder+"amr216/"+grp+"smpl/"
        for j in range(1, 11):
            logfile=logfolder+str(j)+logf
            with open(logfile, 'r') as log:
                logdata= log.read()
                listdata= ast.literal_eval(logdata)
                vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                vfl[0].append(gn+1)
                vfl[1].append(vf)
                vfl[2].append(colors[gn])

    for j in range(11, 21):
        logfile=logfolder+str(j)+logf
        with open(logfile, 'r') as log:
            logdata= log.read()
            listdata= ast.literal_eval(logdata)
            vf=float(listdata[-1]["val/main/RMSE/force"])*1000
            vfl[0].append(gn+2)
            vfl[1].append(vf)
            vfl[2].append(colors[gn+1])

    #Plotting force/RMSE of each Rc & Hidden-layer#
    fig = plt.figure(figsize=(8, 4))
    ax1 = fig.add_subplot(111)
    plt.title("force/RMSE of Amorphous Si")
    ax1.set_ylabel("force/RMSE (meV/$\mathrm{\AA}$)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    plt.rcParams["legend.borderpad"] ='0.3'    #Space between handle & edge
    plt.rcParams["legend.handlelength"] ='1'   #Length of handle
    plt.rcParams["legend.handletextpad"] ='0.2' #Space between handle & label
    plt.rcParams["legend.columnspacing"] ='1'  #Space between columns
    plt.rcParams["legend.labelspacing"] ='0.2' #Space between row of label

    ax1.scatter(vfl[0],vfl[1],c=vfl[2],marker=".")
    left, right = ax1.get_xlim()
    ax1.set_xlim(0, right)
    ax1.axes.xaxis.set_ticks([])

    #ax2 is only for adding legend of run_mq
    ax2 = ax1.twinx() 
    for kk,lbl in enumerate(lbls):
        ax2.scatter(vfl[0][0],vfl[1][0], c=colors[kk], marker=".", label=lbl)
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2,label2,bbox_to_anchor=(1.02, 1),loc='upper left',borderaxespad=0)
    fig.delaxes(ax2)
    plt.savefig(plotfile, bbox_inches='tight')
    plt.close()