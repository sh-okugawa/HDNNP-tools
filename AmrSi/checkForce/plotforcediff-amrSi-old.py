# -*- coding: utf-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt

"""
This script is for plotting G-value of Symm_func (Amorphous Si 315smpl)
 which force vector is much different from other's
"""
def plotG(SFfile, plotfile, fc5list, frcmaxmin, fl, atomn):
    xlb=[]
    colors=["purple","lime","green","cyan","b"]
    colors2=["red","orange"]
    G2=8
    G4=40

    for i in range(G2):
        xlb.append("G2-"+str(i+1))
    for i in range(G4):
        xlb.append("G4-"+str(i+1))

    symt= np.load(SFfile)
    symdtt= symt['sym_func']
    symdL0=len(symdtt)
    symdL1=len(symdtt[0])
    symdL2=len(symdtt[0][0])

    #Plot G-data of 315smpl 
    fig = plt.figure(figsize=(12, 4))
    ax1 = fig.add_subplot(111)
    ttl1=f'[Amorphous-Si: G value] Symm_Func of 315smpl ({symdL0}x{symdL1}x{symdL2})'
    ax1.set_title(ttl1)
    ax1.set_ylabel("Value of G")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    
    #Plot all G-data of symm_func
    for eachsample in symdtt:
        for gdata in eachsample:
            ax1.scatter(xlb, gdata, c='lightgray', marker='.')

    lbls=[]
    #Plot G-gata of symm_func which has max and min force vector
    for nn,frcnum in enumerate(frcmaxmin):
        dtnum=divmod(frcnum,atomn)
        gdata=symdtt[dtnum[0]][dtnum[1]]
        ax1.scatter(xlb, gdata, c=colors2[nn], marker='^')
        numstr=" #"+"{:05d} ".format(frcnum)
        frcstr0="{:f}".format(fl[frcnum][0])
        frcstr1=" {:f}".format(fl[frcnum][1])
        frcstr2=" {:f}".format(fl[frcnum][2])
        lbls.insert(0,numstr+"force["+frcstr0+frcstr1+frcstr2+"]")

    #Plot G-gata of top-5 symm_func which has different force vector from others
    for nn,frcnum in enumerate(fc5list):
        dtnum=divmod(frcnum,atomn)
        gdata=symdtt[dtnum[0]][dtnum[1]]
        ax1.scatter(xlb, gdata, c=colors[nn], marker='x')
        numstr=" #"+"{:05d} ".format(frcnum)
        frcstr0="{:f}".format(fl[frcnum][0])
        frcstr1=" {:f}".format(fl[frcnum][1])
        frcstr2=" {:f}".format(fl[frcnum][2])
        lbls.append(numstr+"force["+frcstr0+frcstr1+frcstr2+"]")
        
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8);

    ax2 = ax1.twinx() ##Only for plotting legend
    for kk in range(5):
        lab="Force-diff No."+str(kk+1)+lbls[6-kk]
        ax2.scatter(xlb,gdata,c=colors[4-kk],marker="x",label=lab)
    lab="Force-max      "+lbls[1]
    ax2.scatter(xlb,gdata,c=colors2[0],marker="^",label=lab)
    lab="Force-min      "+lbls[0]
    ax2.scatter(xlb,gdata,c=colors2[1],marker="^",label=lab)
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2,label2,loc='upper right')
    fig.delaxes(ax2)
    plt.savefig(plotfile)
    print(f'G-data of 315smpl symm_func is plotted')
    plt.close()
         
if __name__ == '__main__': 
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    amrfolder2="/home/okugawa/test-HDNNP-new/HDNNP/Si-amr/amr216/"
    forcefolder=amrfolder+"datas/force/"
    forcefile=forcefolder+"amrsi-315f.txt"
    plotfile=forcefolder+"amrsi-315-G.png"
    histplotfile=forcefolder+"amrsi-315-hist.png"
    atomn=216

    sumdiff,sumd=[],[]
    with open(forcefile, 'r') as f1:
        fclist=[]
        for line in f1:
            linesp=line.split()
            fclist.append([float(linesp[0]),float(linesp[1]),float(linesp[2])])

    #Calculate vector difference from other atom one by one
    fcllen=len(fclist)
    fmax,fmin,frcmaxmin=0,10000,[0,0]
    for nn,fc in enumerate(fclist):
        sumf=0
        for fcc in fclist:
            sumf+=math.sqrt((fcc[0]-fc[0])**2+(fcc[1]-fc[1])**2+(fcc[2]-fc[2])**2)
        sumdiff.append([nn,sumf])
        sumd.append(sumf)
        fcvec=math.sqrt(fc[0]**2+fc[1]**2+fc[2]**2)
        if fcvec>fmax:
            frcmaxmin[0]=nn
            fmax=fcvec
        if fcvec<fmin:
            frcmaxmin[1]=nn
            fmin=fcvec
        if nn % 1000 ==0:
            print(f'Diff calc #{nn}/{fcllen}')

    #Sort vector-diff-sum list 
    sumdiff= sorted(sumdiff, reverse=True, key=lambda x: x[1])

    #Plot histgram of force-vector difference sum
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plttitle="[Amorphous Si 216atom x 315smpl] Sum of force-diff"
    plt.title(plttitle)
    ax.set_xlabel("Sum of force-diff [meV/$\mathrm{\AA}$]")
    plt.hist(sumd, bins=50)
    plt.savefig(histplotfile)
    plt.close()    
    
    #Pick up top-5 different value of force vector
    fc5list=[]
    for i in range(5):
        dtnum=divmod(sumdiff[i][0],atomn)
        smp=dtnum[0]
        atn=dtnum[1]
        print(f'No.{i+1}: #={sumdiff[i][0]} (smpl#:{smp} atom#:{atn}) sum={sumdiff[i][1]}')
        fc5list.insert(0,sumdiff[i][0])  ##add to list in reverse order

    SFfile=amrfolder2+"315smpl/1/data/AmorphousSi216/symmetry_function.npz"
    plotG(SFfile, plotfile, fc5list, frcmaxmin, fclist, atomn)