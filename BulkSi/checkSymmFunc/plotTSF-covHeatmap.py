# -*- coding: utf-8 -*-
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

"""
This script is plotting heatmap of covariance matrix of Train Symm_Func
"""
def plotcovHeatmap(csvfile,SFlb,grp,plotfile,md):
    #Read Covariance matrix from csv file
    with open(csvfile, 'r') as csvs:
        readcsv = csv.reader(csvs, quoting=csv.QUOTE_NONNUMERIC)
        df=pd.DataFrame(data=readcsv, index=SFlb, columns=SFlb)
        
        fig, ax = plt.subplots(figsize=(10, 8)) 
        sns.heatmap(df, cmap='Reds')
        ttl1=f'[{md}/{grp}] Covariance matrix of Train Symm_Func'
        ax.set_title(ttl1)
        plt.savefig(plotfile)
        plt.close()

if __name__ == '__main__': 
    #Plot covariance matrix of Lammps-MD LC7 Train Symm_Func
    LC7Mdistcov="/home/okugawa/HDNNP/Si-190808/result-LC7/Mdist/cov/"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    
    SFlb=["G1"]
    for i in range(1, 25):
        SFlb.append("G2-"+str(i))
    for i in range(1, 17):
        SFlb.append("G4-"+str(i))

    for grp in grps:
        csvfile=LC7Mdistcov+grp+"-cov.csv"
        plotfile=LC7Mdistcov+grp+"-covHeat.png"
        plotcovHeatmap(csvfile,SFlb,grp,plotfile,"Lammps-MD-LC7")
        
    #Plot covariance matrix of AIMD LC7 Train Symm_Func
    LC7Mdistcov="/home/okugawa/HDNNP/Si-190808-md/result-LC7n/Mdist/cov/"
    AIgrps=['0.95','0.97','0.99','1.0','1.01','1.03','1.05','mix']
    
    for grp in AIgrps:
        csvfile=LC7Mdistcov+grp+"-cov.csv"
        plotfile=LC7Mdistcov+grp+"-covHeat.png"
        plotcovHeatmap(csvfile,SFlb,grp,plotfile,"AIMD-LC7")