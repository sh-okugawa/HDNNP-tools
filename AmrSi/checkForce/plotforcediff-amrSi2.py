# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt

"""
This script is for plotting Violin chart of PC1/PC2/PC3 of bs samples
"""

if __name__ == '__main__': 
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    forcefolder=amrfolder+"datas/force/"
    grps=["amrsi-315f"]

    for grp in grps:
        forcefile=forcefolder+grp+".txt"
        fdiff=[]
        sumdiff=[]
    
        with open(forcefile, 'r') as f1:
            fclist=[]
            for line in f1:
                linesp=line.split()
                fclist.append([float(linesp[0]),float(linesp[1]),float(linesp[2])])
    
        for nn,fc in enumerate(fclist):
            fdf=[]
            for fcc in fclist:
                fd=math.sqrt((fcc[0]-fc[0])**2+(fcc[1]-fc[1])**2+(fcc[2]-fc[2])**2)
                fdf.append(fd)
            sumf=sum(fdf)
            sumdiff.append(sumf)
            fdf.insert(0,nn)
            fdf.insert(1,sumf)
            fdiff.append(fdf)

        fdiff= sorted(fdiff, reverse=True, key=lambda x: x[1])

        #Plot Violin chart of MD 1000K/1200K
        plotfile=forcefolder+grp+"-frcHist.png"
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plttitle="["+grp+"] Histgram of Force diff"
        plt.title(plttitle)
        plt.hist(sumdiff, bins=30)
        plt.savefig(plotfile)
        plt.close()
        
        print(f'No.1: #={fdiff[0][0]} sum={fdiff[0][1]}')
        print(f'No.2: #={fdiff[1][0]} sum={fdiff[1][1]}')
        print(f'No.3: #={fdiff[2][0]} sum={fdiff[2][1]}')
        print(f'No.4: #={fdiff[3][0]} sum={fdiff[3][1]}')
        print(f'No.5: #={fdiff[4][0]} sum={fdiff[4][1]}')