# coding: utf-8
import sys
import math
import csv
import matplotlib.pyplot as plt

"""
This script is for comparing FORCE_FC3 data of HDNNP & DFT
 by calculating difference of each element
"""

def readFORCE(FC3file):
    with open(FC3file, mode='r') as FC3:
        lines=FC3.readlines()
        FC3list=[]
        FC3data=[]
        dtnum=0
        
        for lnum,line in enumerate(lines):
            if "# " in line:
                if dtnum!=0:
                    print(f'FC3 file read error: Line#:{lnum} of {FC3file}')
                    sys.exit()

            elif line!="":
                FC3dt=line.split()
                FC3data.append([float(FC3dt[0]),float(FC3dt[1]),float(FC3dt[2])])
                dtnum+=1
                if dtnum==64:
                    FC3list.append(FC3data)
                    FC3data=[]
                    dtnum=0

        if dtnum!=0:
            print(f'FC3 file read error: Line#:{lnum} of {FC3file}')
            sys.exit()
        else:
            return(FC3list)

def Fdiff(f1, f2):
    if len(f1)!=len(f2) or len(f1[0])!=len(f2[0]):
        print(f'Data length Err: Len1={len(f1)} & Len2={len(f2)}')
        sys.exit()
    difflist=[]
    for numi, f1dt in enumerate(f1):
        for numj, f1d in enumerate(f1dt):
            f2d=f2[numi][numj]
            diff=math.sqrt((f1d[0]-f2d[0])**2+(f1d[1]-f2d[1])**2+(f1d[2]-f2d[2])**2)
            difflist.append(diff)
    return(difflist)

if __name__ == '__main__': 
    HDNNPfolder="/home/okugawa/test-HDNNP-new/HDNNP/Si-200917/"
    smallfolder=HDNNPfolder+"small/"
    LC7folder=HDNNPfolder+"1000K-LC7/mix/3500smpl/"
    LC3folder=HDNNPfolder+"1000K-LC3/mix/3000smpl/"
    LC1folder=HDNNPfolder+"1000K-LC1/1500smpl/"
    FC3DFT="/home/okugawa/HDNNP/DFT/FORCES_FC3"
    FC3diffcsv=smallfolder+"result/FC3/FC3diff.csv"
    FC3diffallcsv=smallfolder+"result/FC3/FC3diffall.csv"
    plotfile=smallfolder+"result/FC3diff.png"

    colors=["orange","red","b","green","cyan","brown"]
    lbls=["small-0.5","small-0.99","LC7m-0.5","LC7m-0.99","LC3m-0.99","LC1-0.99"]
    
    DFTdt=readFORCE(FC3DFT)
    FC3diff=[[] for i in range(6)]
    difflisttot=[]
    
    #Compare small's FORCE_FC3
    for i in range(1,21):
        FC3f=smallfolder+str(i)+"/predict-phono3py/FORCES_FC3"
        FC3d=readFORCE(FC3f)
        difflist=Fdiff(DFTdt, FC3d)
        diff=sum(difflist)/len(difflist)
        if i<11:
            FC3diff[0].append(diff)
            difflist.insert(0,"small-0.5-"+str(i))
            difflisttot.append(difflist)
        else:
            FC3diff[1].append(diff)
            difflist.insert(0,"small-0.99-"+str(i-10))
            difflisttot.append(difflist)            

    #Compare LC7mix's FORCE_FC3
    for i in range(1,21):
        FC3f=LC7folder+str(i)+"/predict-phono3py/FORCES_FC3"
        FC3d=readFORCE(FC3f)
        difflist=Fdiff(DFTdt, FC3d)
        diff=sum(difflist)/len(difflist)
        if i>10:
            FC3diff[2].append(diff)
            difflist.insert(0,"LC7mix-0.5-"+str(i-10))
            difflisttot.append(difflist)
        else:
            FC3diff[3].append(diff)
            difflist.insert(0,"LC7mix-0.99-"+str(i))
            difflisttot.append(difflist)

    #Compare LC3mix's FORCE_FC3
    for i in range(1,6):
        FC3f=LC3folder+str(i)+"/predict-phono3py/FORCES_FC3"
        FC3d=readFORCE(FC3f)
        difflist=Fdiff(DFTdt, FC3d)
        diff=sum(difflist)/len(difflist)
        FC3diff[4].append(diff)
        difflist.insert(0,"LC3mix-0.99-"+str(i))
        difflisttot.append(difflist)

    #Compare LC3mix's FORCE_FC3
    for i in range(1,6):
        FC3f=LC1folder+str(i)+"/predict-phono3py/FORCES_FC3"
        FC3d=readFORCE(FC3f)
        difflist=Fdiff(DFTdt, FC3d)
        diff=sum(difflist)/len(difflist)
        FC3diff[5].append(diff)
        difflist.insert(0,"LC1-0.99-"+str(i))
        difflisttot.append(difflist)

    #Save FC3diff data to csv file
    with open(FC3diffcsv, 'w') as Fdcsv:
        writer2 = csv.writer(Fdcsv, lineterminator='\n')
        for i in range(6):
            writer2.writerow(FC3diff[i])

    #Save all of diff data to csv file
    with open(FC3diffallcsv, 'w') as Fdtcsv:
        writer3 = csv.writer(Fdtcsv, lineterminator='\n')
        for diffl in difflisttot:
            writer3.writerow(diffl)
            
    print(f'FORCE_FC3 diff data is saved')

    #Plotting FORCE_RC3 error of each sample from DFT's
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title("FORCE_RC3 error of each sample from DFT's")
    ax1.set_ylabel("Ave of FORCE_RC3 error from DFT's")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    for i in range(4):
        for j in range(10):
            ax1.scatter(i+1,FC3diff[i][j],c=colors[i],marker='.')

    for i in range(4,6):
        for j in range(5):
            ax1.scatter(i+1,FC3diff[i][j],c=colors[i],marker='.')

    ax1.set_xlim(0, 7)
    ax1.set_ylim(0, 0.005)
    plt.xticks(color="None")

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(6):
        ax2.scatter(0,FC3diff[0][0],c=colors[k],marker='.',label=lbls[k])
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right')
    fig.delaxes(ax2)
    plt.savefig(plotfile)
    plt.close()