# -*- coding: utf-8 -*-
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

"""
This script is for plotting G-value of Symm_func (Amorphous Si 315smpl)
 which force vector is much different from other's
"""

def calsumf(SFfile,sumfsavefile):
    symt= np.load(SFfile)
    dervdt= symt['derivative']
    dL0=len(dervdt)
    dL1=len(dervdt[0])
    dL2=len(dervdt[0][0])
    dL3=len(dervdt[0][0][0])
    print(f'Derivative shape = {dL0}x{dL1}x{dL2}x{dL3}')
    
    if dL3/3 != dL1:
        print(f'Derivative shape error: {dL3} is not {dL1}x3')
        sys.exit()
    
    #Calculate sum of force from derivative data
    sumforce, sumfrc=[],[]
    for nn,eachsample in enumerate(dervdt):
        for eachatom in eachsample:
            for eachG in eachatom:
                sumfc=0
                for i in range(0,dL3,3):
                    sumfc+=math.sqrt(eachG[i]**2+eachG[i+1]**2+eachG[i+2]**2)
                sumfrc.append(sumfc)
            sumforce.append(sumfrc)
            sumfrc=[]
        print(f'smpl#{nn}: sum of force from derivative is calculated')
    
    np.savez(sumfsavefile,sumforce=sumforce,L0=dL0,L1=dL1,L2=dL2,L3=dL3)
    return([sumforce,dL0,dL1,dL2,dL3])

def plotsumf(sumforces, plotfolder, fdif5list, fmax5list, fmin5list, fl, atomn):
    xlb=[]
    colors=["b","lime","green","orange","red"]
    G2=8
    G4=40
    sumforce=sumforces[0]
    dL0,dL1,dL2,dL3=sumforces[1],sumforces[2],sumforces[3],sumforces[4]
    ylimlow,ylimup = -0.4, 9.2

    for i in range(G2):
        xlb.append("G2-"+str(i+1))
    for i in range(G4):
        xlb.append("G4-"+str(i+1))

    #Plot G-data of 315smpl 
    fig = plt.figure(figsize=(12, 4))
    ax1 = fig.add_subplot(111)
    ax1.set_ylabel("Sum of force from derivative")
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    ax1.set_ylim(ylimlow,ylimup)
    
    #Plot all sum-of-force data from derivative
    for sumfdata in sumforce:
        ax1.scatter(xlb, sumfdata, c='lightgray', marker='.')
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=90, fontsize=8)
    
    #Plot G-gata of top-5 symm_func which has different force vector from others
    ax2 = ax1.twinx()
    ax2.set_ylim(ylimlow,ylimup)
    ttl1=f'[Amorphous-Si 315smpl] Sum of force from derivative({dL0}x{dL1}x{dL2}x{dL3}) with Top5 of force-diff'
    ax2.set_title(ttl1)
    plotfile=plotfolder+"amrsi-315-deriv-frcdiff.png"
    for nn,frcnum in enumerate(fdif5list):
        gdata=sumforce[frcnum]
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
    ttl1=f'[Amorphous-Si 315smpl] Sum of force from derivative({dL0}x{dL1}x{dL2}x{dL3}) with Top5 of force-max'
    ax3.set_title(ttl1)
    plotfile=plotfolder+"amrsi-315-deriv-frcmax.png"
    for nn,frcnum in enumerate(fmax5list):
        gdata=sumforce[frcnum]
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
    ttl1=f'[Amorphous-Si 315smpl] Sum of force from derivative({dL0}x{dL1}x{dL2}x{dL3}) with Top5 of force-min'
    ax4.set_title(ttl1)
    plotfile=plotfolder+"amrsi-315-deriv-frcmin.png"
    for nn,frcnum in enumerate(fmin5list):
        gdata=sumforce[frcnum]
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
    #plotfile=forcefolder+"amrsi-315-G.png"
    atomn=216

    with open(forcefile, 'r') as f1:
        fclist=[]
        for line in f1:
            linesp=line.split()
            fclist.append([float(linesp[0]),float(linesp[1]),float(linesp[2])])

    savefile=forcefolder+"amrsi-315f-save.npz"
    symt= np.load(savefile)
    sumdiff= symt['sumdiff']
    fcvec= symt['fcvec']

    #Pick up top-5 different value of force vector
    fcdiff5list=[]
    for i in range(5):
        snn=int(sumdiff[i])
        dtnum=divmod(snn,atomn)
        smp=dtnum[0]
        atn=dtnum[1]
        print(f'F-diff No.{i+1}: #={snn} (smpl#:{smp} atom#:{atn})')
        fcdiff5list.insert(0,snn)  ##add to list in reverse order

    #Pick up biggest-5 force vector
    fmax5list=[]
    for i in range(5):
        snn=int(fcvec[i])
        dtnum=divmod(snn,atomn)
        smp=dtnum[0]
        atn=dtnum[1]
        print(f'F-max No.{i+1}: #={snn} (smpl#:{smp} atom#:{atn})')
        fmax5list.insert(0,snn)  ##add to list in reverse order

    #Pick up smallest-5 force vector
    fmin5list=[]
    for i in range(5):
        snn=int(fcvec[(i+1)*-1])
        dtnum=divmod(snn,atomn)
        smp=dtnum[0]
        atn=dtnum[1]
        print(f'F-min No.{i+1}: #={snn} (smpl#:{smp} atom#:{atn})')
        fmin5list.insert(0,snn)  ##add to list in reverse order

    SFfile=amrfolder2+"315smpl/1/data/AmorphousSi216/symmetry_function.npz"
    sumfsavefile=forcefolder+"amrsi-315f-derv-sumfsave.npz"
    symt= np.load(sumfsavefile)
    sumforce= symt['sumforce']
    L0=int(symt['L0'])
    L1=int(symt['L1'])
    L2=int(symt['L2'])
    L3=int(symt['L3'])
    sumforces=[sumforce,L0,L1,L2,L3]
    plotsumf(sumforces, forcefolder, fcdiff5list, fmax5list, fmin5list, fclist, atomn)