# -*- coding: utf-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt

"""
This script is for plotting G-value of Symm_func (Amorphous Si 315smpl)
 which force vector is much different from other's
"""
def plotG(SFfile, plotfolder, fdif5list, fmax5list, fmin5list, fl, atomn):
    xlb=[]
    colors=["b","lime","green","orange","red"]
    G2=8
    G4=40
    ylimlow,ylimup = -0.2, 4.9

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
    ax1.set_ylabel("Value of G")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    ax1.set_ylim(ylimlow,ylimup)
    
    #Plot all G-data of symm_func
    for eachsample in symdtt:
        for gdata in eachsample:
            ax1.scatter(xlb, gdata, c='lightgray', marker='.')
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8)
    
    #Plot G-gata of top-5 symm_func which has different force vector from others
    ax2 = ax1.twinx()
    ax2.set_ylim(ylimlow,ylimup)
    ttl1=f'[Amorphous-Si] Symm_func of 315smpl ({symdL0}x{symdL1}x{symdL2}) with Top5 of force-diff'
    ax2.set_title(ttl1)
    plotfile=plotfolder+"amrsi-315-frcdiff.png"
    for nn,frcnum in enumerate(fdif5list):
        dtnum=divmod(frcnum,atomn)
        gdata=symdtt[dtnum[0]][dtnum[1]]
        numstr=" #"+"{:05d} ".format(frcnum)
        frcstr0="{:f}".format(fl[frcnum][0])
        frcstr1=" {:f}".format(fl[frcnum][1])
        frcstr2=" {:f}".format(fl[frcnum][2])
        lbl="Force-diff No."+str(5-nn)+numstr+"force["+frcstr0+frcstr1+frcstr2+"]"
        ax2.scatter(xlb, gdata, c=colors[nn], marker='x', label=lbl)

    #Plot legend in reversed order
    hans, labs = ax2.get_legend_handles_labels()
    ax2.legend(handles=hans[::-1], labels=labs[::-1], loc='upper right')
    plt.savefig(plotfile)
    fig.delaxes(ax2)
    print(f'G-data of 315smpl symm_func with Force-diff is plotted')

    #Plot G-gata of top-5 symm_func which has max of Force vector 
    ax3 = ax1.twinx()
    ax3.set_ylim(ylimlow,ylimup)
    ttl1=f'[Amorphous-Si] Symm_func of 315smpl ({symdL0}x{symdL1}x{symdL2}) with Top5 of force-max'
    ax3.set_title(ttl1)
    plotfile=plotfolder+"amrsi-315-frcmax.png"
    for nn,frcnum in enumerate(fmax5list):
        dtnum=divmod(frcnum,atomn)
        gdata=symdtt[dtnum[0]][dtnum[1]]
        numstr=" #"+"{:05d} ".format(frcnum)
        frcstr0="{:f}".format(fl[frcnum][0])
        frcstr1=" {:f}".format(fl[frcnum][1])
        frcstr2=" {:f}".format(fl[frcnum][2])
        lbl="Force-max No."+str(5-nn)+numstr+"force["+frcstr0+frcstr1+frcstr2+"]"
        ax3.scatter(xlb, gdata, c=colors[nn], marker='x', label=lbl)

    #Plot legend in reversed order
    hans, labs = ax3.get_legend_handles_labels()
    ax3.legend(handles=hans[::-1], labels=labs[::-1], loc='upper right')
    plt.savefig(plotfile)
    fig.delaxes(ax3)
    print(f'G-data of 315smpl symm_func with Force-max is plotted')

    #Plot G-gata of top-5 symm_func which has min of Force vector 
    ax4 = ax1.twinx()
    ax4.set_ylim(ylimlow,ylimup)
    ttl1=f'[Amorphous-Si] Symm_func of 315smpl ({symdL0}x{symdL1}x{symdL2}) with Top5 of force-min'
    ax4.set_title(ttl1)
    plotfile=plotfolder+"amrsi-315-frcmin.png"
    for nn,frcnum in enumerate(fmin5list):
        dtnum=divmod(frcnum,atomn)
        gdata=symdtt[dtnum[0]][dtnum[1]]
        numstr=" #"+"{:05d} ".format(frcnum)
        frcstr0="{:f}".format(fl[frcnum][0])
        frcstr1=" {:f}".format(fl[frcnum][1])
        frcstr2=" {:f}".format(fl[frcnum][2])
        lbl="Force-min No."+str(5-nn)+numstr+"force["+frcstr0+frcstr1+frcstr2+"]"
        ax4.scatter(xlb, gdata, c=colors[nn], marker='x', label=lbl)

    #Plot legend in reversed order
    hans, labs = ax4.get_legend_handles_labels()
    ax4.legend(handles=hans[::-1], labels=labs[::-1], loc='upper right')
    plt.savefig(plotfile)
    fig.delaxes(ax4)
    print(f'G-data of 315smpl symm_func with Force-max is plotted')
    plt.close()
    
if __name__ == '__main__': 
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    amrfolder2="/home/okugawa/test-HDNNP-new/HDNNP/Si-amr/amr216/"
    forcefolder=amrfolder+"datas/force/"
    forcefile=forcefolder+"amrsi-315f.txt"
    plotfile=forcefolder+"amrsi-315-G.png"
    atomn=216

    sumdiff,sumd,fcvec,fcvc=[],[],[],[]
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
        fcv=math.sqrt(fc[0]**2+fc[1]**2+fc[2]**2)
        fcvec.append([nn,fcv])
        fcvc.append(fcv)
        if nn % 1000 ==0:
            print(f'Diff calc #{nn}/{fcllen}')

    #Sort vector-diff-sum list and force-vector list
    sumdiff= sorted(sumdiff, reverse=True, key=lambda x: x[1])
    fcvec= sorted(fcvec, reverse=True, key=lambda x: x[1])

    #Plot histgram of force-vector difference sum
    fdifhistplotfile=forcefolder+"amrsi-315-fdif-hist.png"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plttitle="[Amorphous Si 216atom x 315smpl] Sum of force-diff"
    plt.title(plttitle)
    ax.set_xlabel("Sum of force-diff [meV/$\mathrm{\AA}$]")
    plt.hist(sumd, bins=50)
    plt.savefig(fdifhistplotfile)
    plt.close()    
    
    #Plot histgram of force-vector
    fvechistplotfile=forcefolder+"amrsi-315-fvec-hist.png"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plttitle="[Amorphous Si 216atom x 315smpl] Force vector"
    plt.title(plttitle)
    ax.set_xlabel("Force vector [meV/$\mathrm{\AA}$]")
    plt.hist(fcvc, bins=50)
    plt.savefig(fvechistplotfile)
    plt.close()    

    #Pick up top-5 different value of force vector
    fcdiff5list=[]
    for i in range(5):
        dtnum=divmod(sumdiff[i][0],atomn)
        smp=dtnum[0]
        atn=dtnum[1]
        print(f'F-diff No.{i+1}: #={sumdiff[i][0]} (smpl#:{smp} atom#:{atn}) sum={sumdiff[i][1]}')
        fcdiff5list.insert(0,sumdiff[i][0])  ##add to list in reverse order

    #Pick up biggest-5 force vector
    fmax5list=[]
    for i in range(5):
        dtnum=divmod(fcvec[i][0],atomn)
        smp=dtnum[0]
        atn=dtnum[1]
        print(f'F-max No.{i+1}: #={fcvec[i][0]} (smpl#:{smp} atom#:{atn}) frc={fcvec[i][1]}')
        fmax5list.insert(0,fcvec[i][0])  ##add to list in reverse order

    #Pick up smallest-5 force vector
    fmin5list=[]
    for i in range(5):
        dtnum=divmod(fcvec[(i+1)*-1][0],atomn)
        smp=dtnum[0]
        atn=dtnum[1]
        print(f'F-min No.{i+1}: #={fcvec[(i+1)*-1][0]} (smpl#:{smp} atom#:{atn}) frc={fcvec[(i+1)*-1][1]}')
        fmin5list.insert(0,fcvec[(i+1)*-1][0])  ##add to list in reverse order

    SFfile=amrfolder2+"315smpl/1/data/AmorphousSi216/symmetry_function.npz"
    plotG(SFfile, forcefolder, fcdiff5list, fmax5list, fmin5list, fclist, atomn)
