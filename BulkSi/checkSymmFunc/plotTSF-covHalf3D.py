# -*- coding: utf-8 -*-
import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
This script is plotting 3D covariance matrix of Train Symm_Func 
"""
def plotcov3D(covl,grp,plotfile,md):
    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    SFlb=["G1"]
    for i in range(1, 25):
        SFlb.append("G2-"+str(i))
    for i in range(1, 17):
        SFlb.append("G4-"+str(i))
    lenSF= len(SFlb)
    SFtick = [i for i in range(lenSF)]

    xpos,ypos= [],[]
    j= lenSF
    for i in range(lenSF):
        xpos.extend([k for k in range(i,lenSF)])
        ypos.extend([i]*j)
        j-=1
    zpos=np.zeros(len(xpos))
    dx=np.full(len(xpos), 0.1)
    dy=np.full(len(ypos), 0.1)
    dz=covl
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz)

    plt.xticks(SFtick, SFlb)
    plt.yticks(SFtick, SFlb)
    ttl1=f'[{md}/{grp}] Covariance matrix of Train Symm_Func'
    ax.set_title(ttl1)
    ax.grid(True)
    xlabels = ax.get_xticklabels()
    plt.setp(xlabels, rotation=90, fontsize=8);
    ylabels = ax.get_yticklabels()
    plt.setp(ylabels, rotation=90, fontsize=8);
    plt.savefig(plotfile)
    plt.close()

def readcovhalf(csvfile):
    #Read TC err from csv file
    with open(csvfile, 'r') as csvs:
        readcsv = csv.reader(csvs, quoting=csv.QUOTE_NONNUMERIC)
        covlh = []
        for i,row in enumerate(readcsv):
            covlh.extend(row[i:])
    return(covlh)

if __name__ == '__main__': 
    #Plot covariance matrix of Lammps-MD LC7 Train Symm_Func
    LC7Mdistcov="/home/okugawa/HDNNP/Si-190808/result-LC7/Mdist/cov/"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    
    for grp in grps:
        csvfile=LC7Mdistcov+grp+"-cov.csv"
        covlh=readcovhalf(csvfile)
        plotfile=LC7Mdistcov+grp+"-cov3D.png"
        plotcov3D(covlh,grp,plotfile,"Lammps-MD-LC7")
        
    #Plot covariance matrix of AIMD LC7 Train Symm_Func
    LC7Mdistcov="/home/okugawa/HDNNP/Si-190808-md/result-LC7n/Mdist/cov/"
    AIgrps=['0.95','0.97','0.99','1.0','1.01','1.03','1.05','mix']
    
    for grp in AIgrps:
        csvfile=LC7Mdistcov+grp+"-cov.csv"
        covlh=readcovhalf(csvfile)
        plotfile=LC7Mdistcov+grp+"-cov3D.png"
        plotcov3D(covlh,grp,plotfile,"AIMD-LC7")