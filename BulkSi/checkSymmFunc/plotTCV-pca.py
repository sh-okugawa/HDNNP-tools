# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv

"""
This script is for plotting training curve of gs & each PCA
"""

def plotTCV(tcvfolder, clr, lbl):
    for j in range(1,11):
        PCfile=tcvfolder+"-"+str(j)+".csv"
        
        with open(PCfile,'r') as f1:
            traincvdt = csv.reader(f1)
            epl=[]
            vfl=[]
            for tcv in traincvdt:
                epl.append(int(tcv[0]))
                vfl.append(float(tcv[2]))
        
            if j==10:
                ln1 = ax1.plot(epl,vfl,color=clr,label=lbl)
            else:
                ln1 = ax1.plot(epl,vfl, color=clr)
        
if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/Si-190808/"
    gstcv=root+"result/traincv/d20n50"
    pcatcv=root+"pca-result/traincv/"
    grps=["p30","p20","p15","p10","noPCA"]
    colors=["b","green","orange","red","grey"]
    labels=["41->30","41->20","41->15","41->10","no PCA"]
    plotfile=pcatcv+"plot/all-tcv.png"

    #Plot KDE chart of bs1-8
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("Training curve of all PCA decomposition (data=700)")
    ax1.set_xlabel('epoch')
    ax1.set_ylabel('force/RMSE (meV/A)')
    ax1.set_ylim(20,140)
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'

    #plot training curve of gs
    clr="black"
    lbl="41->41"
    plotTCV(gstcv, clr, lbl)
        
    #plot traing curve of each PCA
    for num,grp in enumerate(grps):
        clr=colors[num]
        lbl=labels[num]
        tcvfolder=pcatcv+grp
        plotTCV(tcvfolder,  clr, lbl)
        
    ax1.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=1, fontsize=9)
    plt.savefig(plotfile)
    plt.close()