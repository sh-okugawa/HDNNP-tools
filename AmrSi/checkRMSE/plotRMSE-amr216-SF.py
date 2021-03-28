# -*- coding: utf-8 -*-
import ast,sys
import numpy as np
import matplotlib.pyplot as plt

"""
This script is for plotting force/RMSE of amrSi103040-3000.xyz with
 3 kind of Symm_func (org/SMZ/Li) and 4 kind of Rc (6.0/6.5/7.0/7.5)
"""

def readvf(logfolder):
    vfl=[]
    for j in range(1, 11):
        logfile=logfolder+"/"+str(j)+"/output/AmorphousSi216/training.log"
        with open(logfile, 'r') as log:
            logdata= log.read()
            listdata= ast.literal_eval(logdata)
            vf=float(listdata[-1]["val/main/RMSE/force"])*1000
            vfl.append(vf)
    return(vfl)

def plotG(SFfile, outfolder, SF, Rc):
    xlb=[]
    clr=[]
    if SF=="org":
        G2=24
        G4=16
    elif SF=="SMZ":
        G2=6
        G4=18
    elif SF=="Li":
        G2=8
        G4=40
    else:
        print(f'Symm_func error: {SF} is unknown')
        sys.exit()

    if SF=="org":
        xlb.append("G1")
        clr.append("cyan")
    for i in range(G2):
        xlb.append("G2-"+str(i+1))
        clr.append("b")
    for i in range(G4):
        xlb.append("G4-"+str(i+1))
        clr.append("g")

    plotfile=outfolder+SF+"-"+Rc+"-Gdata.png"
    symt= np.load(SFfile)
    symdtt= symt['sym_func']

    #Plot G-data of Train 
    fig = plt.figure(figsize=(12, 4))
    ax1 = fig.add_subplot(111)
    stnparr=np.array(symdtt)
    ttl1=f'[Amorphous-Si: G value] Symm_Func:{SF} & Rc:{Rc} ({stnparr.shape})'
    ax1.set_title(ttl1)
    ax1.set_ylabel("Value of G")
    ax1.grid(True)
    for sn,eachsample in enumerate(symdtt):
        if sn % 5 ==0:    ## pick up only 1 of 5 sample for efficiency
            for gdata in eachsample:
                ax1.scatter(xlb, gdata, c=clr, marker='.')
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8);
    plt.savefig(plotfile)
    print(f'G-data of {SF}-{Rc}) is plotted')
    plt.close()
            
if __name__ == '__main__':
    amrfolder="/home/okugawa/HDNNP/Si-amr/amr216/1500-103040smpl/"
    SFfolder=amrfolder+"SymF/SF/"
    rcfolder=amrfolder+"SymF/Rc/"
    sfgrps=["org","SMZ"]
    rcgrps=["6.0","7.0","7.5"]
    xlbs=['org-6.5','SMZ-6.5','Li-6.5','Li-6.0','Li-7.0','Li-7.5']
    colors=["red","orange","green","lime","b","cyan"]
    
    plotfolder=amrfolder+"SymF/result/"
    
    #Read force/RMSE data from log file
    sfnumb=1
    vflist=[]
    for sfg in sfgrps:
        logfolder=SFfolder+sfg
        vfl=readvf(logfolder)
        vflist.append([vfl,[sfnumb for i in range(10)]])
        sfnumb+=1

    vfl=readvf(amrfolder)
    vflist.append([vfl,[sfnumb for i in range(10)]])
    sfnumb+=1        
    
    for rcg in rcgrps:  
        logfolder=rcfolder+rcg
        vfl=readvf(logfolder)
        vflist.append([vfl,[sfnumb for i in range(10)]])
        sfnumb+=1
        
    #Plotting force/RMSE of each Symm_func & Rc
    plotfile=plotfolder+"amrSi-fRMSE-SF.png"
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("force/RMSE of Amorphous Si 1500 sample")
    ax1.set_ylabel("force/RMSE (meV/$\mathrm{\AA}$)")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for nn,vfdt in enumerate(vflist):
        clr=colors[nn]
        ax1.scatter(vfdt[1],vfdt[0],c=clr,marker='.')
    ax1.set_xlim(0, sfnumb)
    ax1.axes.xaxis.set_ticks([])

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(6):
        ax2.scatter(vfdt[1][0],vfdt[0][0],c=colors[k],marker='.',label=xlbs[k])
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2,label2,bbox_to_anchor=(1.02, 1),loc='upper left',
               borderaxespad=0,title='Symm_F & Rc')
    fig.delaxes(ax2)
    plt.savefig(plotfile, bbox_inches='tight')
    plt.close()

    #Plotting G-data of each Symm_func & Rc
    for sfg in sfgrps:
        SFfile=SFfolder+sfg+"/1/data/AmorphousSi216/symmetry_function.npz"
        plotG(SFfile, plotfolder, sfg, "6.5")

    SFfile=amrfolder+"1/data/AmorphousSi216/symmetry_function.npz"
    plotG(SFfile, plotfolder, "Li", "6.5")
    
    for rcg in rcgrps:  
        SFfile=rcfolder+rcg+"/1/data/AmorphousSi216/symmetry_function.npz"    
        plotG(SFfile, plotfolder, "Li", rcg)