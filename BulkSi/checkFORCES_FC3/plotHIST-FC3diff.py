# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import csv

"""
This script is for plotting Histgram chart of PC1 of MD 1000K-LCx4
"""

if __name__ == '__main__': 
    smallfolder="/home/okugawa/test-HDNNP-new/HDNNP/Si-200917/small/"
    FC3diffallcsv=smallfolder+"result/FC3/FC3diffall.csv"
    plotfolder=smallfolder+"result/FC3/hist/"

    #Read FC3 data file and plot histgram
    with open(FC3diffallcsv,'r') as f1:
        difflist = csv.reader(f1)
        diffl = [i*1000 for i in difflist[0]]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plttitle="["+dataname+"] Histgram of FC3 diff from DFT"
        plt.title(plttitle)
        plt.ylim(300)
        plt.hist(row, bins=30)
        plt.savefig(plotfile)
        plt.close()

"""
        for row in difflist:
            dataname=row[0]
            plotfile=plotfolder+dataname+".png"
            row.pop(0)
            difflen=len(row)
            
            fig = plt.figure()
            ax = fig.add_subplot(111)
            plttitle="["+dataname+"] Histgram of FC3 diff from DFT"
            plt.title(plttitle)
            plt.hist(row, bins=30)
            plt.savefig(plotfile)
            plt.close()
            print(f'FC3 diff histgram of {dataname}[{difflen}] is plotted')
"""