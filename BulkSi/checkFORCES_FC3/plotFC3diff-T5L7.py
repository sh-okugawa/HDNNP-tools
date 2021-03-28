# coding: utf-8
import sys
import math
import csv
import matplotlib.pyplot as plt

"""
This script is for comparing FORCE_FC3 data of T5L7 and DFT's
 by calculating difference [Euclid distance] of each element
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
    T5L7folder="/home/okugawa/HDNNP/Si-200917/T5L7/"
    smallfolder="/home/okugawa/HDNNP/Si-200917/small/"
    FC3DFT="/home/okugawa/HDNNP/DFT/FORCES_FC3"
    FC3diffcsv=T5L7folder+"result/FC3/FC3diff.csv"
    FC3diffallcsv=T5L7folder+"result/FC3/FC3diffall.csv"
    plotfile=T5L7folder+"result/FC3/FC3diff.png"

    grps= ["TH3-L7","TH3-L79","TH3-LM3","TM3-L7","TM3-L79","TM3-LM3",
           "TL3-L7","TL3-L79","TL3-LM3","all60"]
    colors=["b","b","cyan","green","green","lime","red","red","orange",
            "brown","grey"]
    marks=["x",".",".","x",".",".","x",".",".","x","x"]
    lbls=["T:H3-L:7(2100)","T:H3-L:7(900)","T:H3-L:3(900)",
          "T:M3-L:7(2100)","T:M3-L:7(900)","T:M3-L:3(900)",
          "T:L3-L:7(2100)","T:L3-L:7(900)","T:L3-L:3(900)",
          "T:5-L:7(2100)","small(2100)"]

    DFTdt=readFORCE(FC3DFT)
    FC3diff=[[] for i in range(11)]
    difflisttot=[]
    
    #Compare T5L7's FORCE_FC3
    for i,grp in enumerate(grps):
        for j in range(1, 11):
            dataname=grp+"-"+str(j)
            datadir= T5L7folder+grp+"/"+str(j)
            FC3f=T5L7folder+grp+"/"+str(j)+"/predict-phono3py/FORCES_FC3"
            FC3d=readFORCE(FC3f)
            difflist=Fdiff(DFTdt, FC3d)
            diff=sum(difflist)/len(difflist)
            FC3diff[i].append(diff)
            difflist.insert(0,grp+"-"+str(j+1))
            difflisttot.append(difflist)
        print(f"FORCE_FC3 of {grp} is compared with DFT's")            

    #Compare small's FORCE_FC3
    for j in range(11,21):
        FC3f=smallfolder+str(j)+"/predict-phono3py/FORCES_FC3"
        FC3d=readFORCE(FC3f)
        difflist=Fdiff(DFTdt, FC3d)
        diff=sum(difflist)/len(difflist)
        FC3diff[i+1].append(diff)
        difflist.insert(0,"small-"+str(j-10))
        difflisttot.append(difflist)
    print(f"FORCE_FC3 of small is compared with DFT's")            

    #Save FC3diff data to csv file
    with open(FC3diffcsv, 'w') as Fdcsv:
        writer2 = csv.writer(Fdcsv, lineterminator='\n')
        for i in range(11):
            writer2.writerow(FC3diff[i])

    #Save all of diff data to csv file
    with open(FC3diffallcsv, 'w') as Fdtcsv:
        writer3 = csv.writer(Fdtcsv, lineterminator='\n')
        for diffl in difflisttot:
            writer3.writerow(diffl)
            
    print(f'FORCE_FC3 diff data are saved')

    #Plotting FORCE_FC3 error of each sample from DFT's
    fig = plt.figure(figsize=(7, 5))
    ax1 = fig.add_subplot(111)
    plt.title("Ave of FORCE_FC3 error of each sample from DFT's")
    ax1.set_ylabel("Ave of FORCE_FC3 error from DFT's")
    ax1.text(0.5, 0.0019, "[Mixing Beta=0.99]")
    ax1.grid(axis='y')
    plt.rcParams["legend.edgecolor"] ='green'
    plt.rcParams["legend.borderpad"] ='0.3'    #Space between handle & edge
    plt.rcParams["legend.handlelength"] ='1'   #Length of handle
    plt.rcParams["legend.handletextpad"] ='0.2' #Space between handle & label
    plt.rcParams["legend.columnspacing"] ='1'  #Space between columns
    plt.rcParams["legend.labelspacing"] ='0.2' #Space between row of label

    for i in range(11):
        for j in range(10):
            ax1.scatter(i+1,FC3diff[i][j],c=colors[i],marker=marks[i])

    ax1.set_xlim(0, 16.5)
    ax1.set_ylim(0.0006, 0.002)
    plt.xticks(color="None")

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(11):
        ax2.scatter(0,FC3diff[0][0],c=colors[k],marker=marks[k],label=lbls[k])
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper right')
    fig.delaxes(ax2)

    plt.savefig(plotfile)
    print(f'FORCE_FC3 diff data are plotted')
    plt.close()