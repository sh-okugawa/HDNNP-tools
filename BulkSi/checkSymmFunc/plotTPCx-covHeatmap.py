# -*- coding: utf-8 -*-
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

"""
This script is plotting heatmap of covariance matrix of PCx of Train Symm_Func
"""
def plotcovHeatmap(csvfile,SFlb,grp,plotfile,md):
    #Read Covariance matrix from csv file
    with open(csvfile, 'r') as csvs:
        readcsv = csv.reader(csvs, quoting=csv.QUOTE_NONNUMERIC)
        df=pd.DataFrame(data=readcsv, index=SFlb, columns=SFlb)
        
        fig, ax = plt.subplots(figsize=(10, 8)) 
        sns.heatmap(df, cmap='Reds')
        ttl1=f'[{md}/{grp}] Covariance matrix of Train PCx'
        ax.set_title(ttl1)
        plt.savefig(plotfile)
        plt.close()

if __name__ == '__main__': 
    PCxlb=[]
    for i in range(1, 42):
        PCxlb.append("PC"+str(i))
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
    
    #Plot covariance matrix of Lammps-MD LC7 Train Symm_Func
    LC7Mdistcov="/home/okugawa/HDNNP/Si-190808/result-LC7/Mdist/cov/"
    for grp in grps:
        csvfile=LC7Mdistcov+grp+"-PCx-cov.csv"
        plotfile=LC7Mdistcov+grp+"-PCx-covHeat.png"
        plotcovHeatmap(csvfile,PCxlb,grp,plotfile,"Lammps-MD-LC7")