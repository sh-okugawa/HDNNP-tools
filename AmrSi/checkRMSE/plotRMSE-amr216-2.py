# -*- coding: utf-8 -*-
import ast
import matplotlib.pyplot as plt

"""
This script is for plotting force/RMSE of Amorphous-Si samples
"""
            
if __name__ == '__main__':
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    grps=['105','315','786','471']
    colors=["red","green","lime","b","cyan","black"]
    lbls=["105smpl","315smpl","315smpl (org SF)","786smpl","786smpl (orgSF)","471smpl"]
    
    plotfile=amrfolder+"result/amrSi-fRMSE-2.png"
    logf="/output/AmorphousSi216/training.log"
    
    #Read force/RMSE data from log file
    rmse = []
    grpnum = 1
    for grp in grps:
        vfl=[[],[]]
        for j in range(1, 11):
            logfile=amrfolder+"amr216/"+grp+"smpl/"+str(j)+logf
            with open(logfile, 'r') as log:
                logdata= log.read()
                listdata= ast.literal_eval(logdata)
                vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                vfl[0].append(grpnum)
                vfl[1].append(vf)
        rmse.append(vfl)
        grpnum+=1

        if grp=="315" or grp=="786":
            vfl=[[],[]]
            for j in range(11, 21):
                logfile=amrfolder+"amr216/"+grp+"smpl/"+str(j)+logf
                with open(logfile, 'r') as log:
                    logdata= log.read()
                    listdata= ast.literal_eval(logdata)
                    vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                    vfl[0].append(grpnum)
                    vfl[1].append(vf)
            rmse.append(vfl)
            grpnum+=1
       
    #Plotting force/RMSE of each Rc & Hidden-layer#
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("force/RMSE of Amorphous Si")
    ax1.set_ylabel("force/RMSE (meV/ang)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for i in range(6):
        clr=colors[i]
        lbl=lbls[i]
        ax1.scatter(rmse[i][0],rmse[i][1],c=clr,marker='.',label=lbl)

    left, right = ax1.get_xlim()
    ax1.set_xlim(0.5, right*1.2)
    ax1.axes.xaxis.set_ticks([])
    ax1.legend()
    plt.savefig(plotfile)
    plt.close()