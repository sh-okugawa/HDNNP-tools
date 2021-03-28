# -*- coding: utf-8 -*-
import ast
import matplotlib.pyplot as plt

"""
This script is for plotting force/RMSE of Amorphous-Si samples
"""
            
if __name__ == '__main__':
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    grps=['105','105-3','105-4','315','471','786','500','1000','1471']
    colors=["red","orange","hotpink","purple","brown","green","lime","b",
            "deepskyblue","olive","cyan"]
    lbls1=["105smpl (r_mq=1000)","105smpl (r_mq=5000)","105smpl (r_mq=10000)",
           "315smpl (r_mq:mix)","315smpl (r_mq:mix)","471smpl","471smpl",
           "786smpl (315+471)","786smpl (315+471)","500smpl (r_mq=1000)","500smpl (r_mq=1000)",
           "1000smpl (r_mq=1000)","1000smpl (r_mq=1000)",
           "1471smpl (1000+471)","1471smpl (1000+471)",
           "1000smpl (mixBeta=0.8)","1000smpl (mixBeta=0.5)",]
    lbls2=["SymF:Li","SymF:Org"]
    marks=[".","x"]
    
    plotfile=amrfolder+"result/amrSi-fRMSE-all2.png"
    logf="/output/AmorphousSi216/training.log"
    
    #Read force/RMSE data from log file
    rmse = []
    grpnum = 1
    clrnum = 0
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
        rmse.append([vfl,clrnum,marks[0]])
        grpnum+=1
        clrnum+=1

        if not "105" in grp:
            vfl=[[],[]]
            for j in range(11, 21):
                logfile=amrfolder+"amr216/"+grp+"smpl/"+str(j)+logf
                with open(logfile, 'r') as log:
                    logdata= log.read()
                    listdata= ast.literal_eval(logdata)
                    vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                    vfl[0].append(grpnum)
                    vfl[1].append(vf)
            rmse.append([vfl,clrnum-1,marks[1]])
            grpnum+=1
       
    for i in range(20,40,10):
        vfl=[[],[]]
        for j in range(1, 11):
            logfile=amrfolder+"amr216/1000smpl/"+str(i+j)+logf
            with open(logfile, 'r') as log:
                logdata= log.read()
                listdata= ast.literal_eval(logdata)
                vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                vfl[0].append(grpnum)
                vfl[1].append(vf)
        rmse.append([vfl,clrnum,marks[0]])
        grpnum+=1
        clrnum+=1

    #Plotting force/RMSE of each Rc & Hidden-layer#
    fig = plt.figure(figsize=(8, 4))
    ax1 = fig.add_subplot(111)
    plt.title("force/RMSE of Amorphous Si")
    ax1.set_ylabel("force/RMSE (meV/ang)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    plt.rcParams["legend.borderpad"] ='0.3'    #Space between handle & edge
    plt.rcParams["legend.handlelength"] ='1'   #Length of handle
    plt.rcParams["legend.handletextpad"] ='0.2' #Space between handle & label
    plt.rcParams["legend.columnspacing"] ='1'  #Space between columns
    plt.rcParams["legend.labelspacing"] ='0.2' #Space between row of label
    for i,rm in enumerate(rmse):
        clr=colors[rmse[i][1]]
        if rmse[i][2]=='.':
            ax1.scatter(rmse[i][0][0],rmse[i][0][1],c=clr,
                        marker=rmse[i][2],label=lbls1[i])
        else:
            ax1.scatter(rmse[i][0][0],rmse[i][0][1],c=clr,
                        marker=rmse[i][2])

    left, right = ax1.get_xlim()
    ax1.set_xlim(0, right)
    ax1.set_ylim(125, 175)
    ax1.axes.xaxis.set_ticks([])
    leg1=ax1.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

    #ax2 is only for adding legend of run_mq
    ax2 = ax1.twinx() 
    for kk,lb2 in enumerate(lbls2):
        ax2.scatter(0,0, c="black", marker=marks[kk], label=lb2)
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc="upper right", ncol=2)
    fig.delaxes(ax2)
    ax1.add_artist(leg1)
    plt.savefig(plotfile, bbox_inches='tight')
    plt.close()