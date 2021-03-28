# -*- coding: utf-8 -*-
import csv
import ast
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

"""
This script is made to output csv file by gathering 
1) force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
2) train curve data (epoch, trained force/RMSE, validated, difference))
from RMSE/TC data of Si-Amorphous-216atom samples (421samples)
And plot symm_func and PC1/PC2 KDE chart
"""

def gatherplotTCV(logfile,traincvfile,plotfile,dataname):
    with open(logfile, 'r') as log:
        logdata= log.read()
        listdata= ast.literal_eval(logdata)
        listlen= len(listdata)
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
        plt.title("["+dataname+"] Training curve")
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
        
def plotG(symdtt, grp, plotfile, xlb, clr, md):
    #Plot G-data of Train 
    fig = plt.figure(figsize=(12, 4))
    ax1 = fig.add_subplot(111)
    stnparr=np.array(symdtt)
    ttl1=f'[{md}/{grp}] Train({stnparr.shape}) Symm_Func G value'
    ax1.set_title(ttl1)
    ax1.set_ylabel("Value of G")
    ax1.grid(True)
    for eachsample in symdtt:
        for gdata in eachsample:
            ax1.scatter(xlb, gdata, c=clr, marker='.')
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8);
    plt.savefig(plotfile)
    print(f'G-data of {grp} Train({symdtt.shape}) is plotted')
    plt.close()
    
def gatherG(SFfile, outfolder, grp, md):
    xlb=[]
    clr=[]
    for i in range(1, 9):
        xlb.append("G2-"+str(i))
        clr.append("g")
    for i in range(1, 41):
        xlb.append("G4-"+str(i))
        clr.append("c")

    plotfile=outfolder+"amr216-"+grp+"-Gdata.png"
    symt= np.load(SFfile)
    symdtt= symt['sym_func']

    plotG(symdtt, grp, plotfile, xlb, clr, md)
        
def makePC123(dtsetfile, outfile, grp):
    dtset= np.load(dtsetfile, allow_pickle=True)
    #allow_pickle op is for adapting spec change of numpy 1.16.3 and later
    dts= dtset['dataset']
    dataset0=[]

    for dt in dts:
        dt0=dt['inputs/0']
        dataset0.append(dt0)

    dim0=len(dataset0)
    dim1=len(dataset0[0])
    dim2=len(dataset0[0][0])
    
    with open(outfile, 'w') as f1:
        for dt64 in dataset0:
            for dt in dt64:
                wdt=str(dt[0])+" "+str(dt[1])+" "+str(dt[2])+"\n"
                f1.write(wdt)
                
    print(f'Saved PC1/PC2/PC3 data of {grp}: Shape= {dim0}x{dim1}x{dim2}')
    
def plotKDE(PCfile,plotfile,grpname):
    PC123dt = np.loadtxt(PCfile)
    PCdt= pd.DataFrame(PC123dt, columns=['PC1','PC2','PC3'])

    #Plot KDE chart of PC1/PC2 
    plt.style.use('default')
    sns.set()
    sns.set_style('whitegrid')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plttitle="["+grpname+"]"
    ax= sns.jointplot(data=PCdt, x='PC1', y='PC2', kind='kde')
    plt.text(-10, 0.24, plttitle, size = 15, color = "black")
    plt.savefig(plotfile)
    print(f'KDE chart of {grpname} is plotted')
    plt.close('all')
            
if __name__ == '__main__': 
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    grps=['2','3']
    
    plotdir=amrfolder+"result/grpplot/"
    traindir=amrfolder+"result/traincv/"
    PC123dir=amrfolder+"result/PC123/"
    
    for grp in grps:
        #Plot training curve 
        logfile= amrfolder+"amr216/"+grp+"/output/AmorphousSi216/training.log"
        traincvfile= traindir+"amr216-"+grp+".csv"
        plotfile= traindir+"plot/amr216-"+grp+".png"
        gatherplotTCV(logfile,traincvfile,plotfile,grp)
        print(f'Training curve of amr216-{grp} is plotted')
        
        #Plot Symm_func
        SFfile=amrfolder+"amr216/"+grp+"/data/AmorphousSi216/symmetry_function.npz"
        outfolder=amrfolder+"result/grpplot/symf/"
        gatherG(SFfile, outfolder, grp, "Si-Amorphous")
        print(f'Symm_func of amr216-{grp} is plotted')

        #Correct PC1/PC2/PC3 data
        dtsetfile=amrfolder+"amr216/"+grp+"/data/AmorphousSi216/preprocd_dataset.npz"
        PC123file=PC123dir+"amr216-"+grp+"-PC123.txt"
        makePC123(dtsetfile, PC123file, grp)
        print(f'PC123.txt of amr216-{grp} is saved')

        #Plot KDE chart of PC1&PC2
        KDEfile=PC123dir+"amr216-"+grp+"-KDE.png"
        plotKDE(PC123file,KDEfile,grp)
        print(f'KDE chart of amr216-{grp} is plotted')