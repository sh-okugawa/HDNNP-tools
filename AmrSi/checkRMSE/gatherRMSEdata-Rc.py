# -*- coding: utf-8 -*-
import ast
import matplotlib.pyplot as plt

"""
This script is for plotting force/RMSE of 6-Rc & 4-Hidden layers
"""
            
if __name__ == '__main__':
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    rcfolder=amrfolder+"amr216/Rc/"
    xlb=['6.5','6.7','6.9','7.1','7.3','7.5']
    Hlayers=['2','3','4','5']
    colors=["red","orange","lime","b"]
    
    plotdir=amrfolder+"result/grpplot/"
    
    #Read force/RMSE data from log file
    vfl=[[] for n in range(4)]
    for i in range(6):
        for j in range(1, 5):
            logfile=rcfolder+str(i)+"/"+str(j)+"/output/AmorphousSi216/training.log"
            with open(logfile, 'r') as log:
                logdata= log.read()
                listdata= ast.literal_eval(logdata)
                vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                vfl[j-1].append(vf)

    #Plotting force/RMSE of each Rc & Hidden-layer#
    allplotfile=plotdir+"Rc6HL4.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("force/RMSE of Rcx6 HLx4 MD 1000K-LC7mix")
    ax1.set_xlabel("Rc")
    ax1.set_ylabel("force/RMSE (meV/A)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for nn,vfdt in enumerate(vfl):
        clr=colors[nn]
        ax1.scatter(xlb,vfdt,c=clr,marker='o')

    left, right = ax1.get_xlim()
    ax1.set_xlim(-0.1, right*1.2)

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(4):
        ax2.scatter(xlb,vfdt,c=colors[k],marker='o',label=Hlayers[k])
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right',title='H-layer#')
    fig.delaxes(ax2)
    plt.savefig(allplotfile)
    plt.close()