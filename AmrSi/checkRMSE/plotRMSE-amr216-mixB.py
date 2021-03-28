# -*- coding: utf-8 -*-
import ast
import matplotlib.pyplot as plt

"""
This script is for plotting force/RMSE of Amorphous-Si samples
"""
            
if __name__ == '__main__':
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    grps=[1, 21, 31]
    colors=["b","green","red"]
    lbls=["Mix Beta=0.99","Mix Beta=0.8","Mix Beta=0.5"]
    
    plotfile=amrfolder+"result/amrSi-fRMSE-mixB.png"
    logf="/output/AmorphousSi216/training.log"
    
    #Read force/RMSE data from log file
    vfl=[[],[],[]]
    for i,grp in enumerate(grps):
        for j in range(10):
            logfile=amrfolder+"amr216/1000-10smpl/"+str(grp+j)+logf
            with open(logfile, 'r') as log:
                logdata= log.read()
                listdata= ast.literal_eval(logdata)
                vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                vfl[0].append(i+1)
                vfl[1].append(vf)
                vfl[2].append(colors[i])

    #Plotting force/RMSE of each Rc & Hidden-layer#
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("[Amorphous Si] force/RMSE @ Mixing Beta=0.99/0.8/0.5")
    ax1.set_ylabel("force/RMSE (meV/$\mathrm{\AA}$)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    ax1.scatter(vfl[0],vfl[1],c=vfl[2],marker=".")
    left, right = ax1.get_xlim()
    ax1.set_xlim(0, right*1.3)
    ax1.set_ylim(125, 162)
    ax1.axes.xaxis.set_ticks([])
    bbox_dict = dict(edgecolor="gray", fill=False)
    ax1.text(1.5, 127, "5scale-mix, 1000samples, Symm_func=Li", bbox=bbox_dict)

    #ax2 is only for adding legend of run_mq
    ax2 = ax1.twinx() 
    for i,lbl in enumerate(lbls):
        ax2.scatter(vfl[0][0],vfl[1][0], c=colors[i], marker=".", label=lbl)
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc="upper left")
    fig.delaxes(ax2)
    plt.savefig(plotfile, bbox_inches='tight')
    plt.close()