# -*- coding: utf-8 -*-
import csv
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

"""
This script is for calculating Linear-Regression and correlation of
force/RMSE and TC by sklearn linear-model, then plot them 
"""

def calcplotcoeff(rstfile,plotfile1,title1,plotfile2,title2):
    clf = linear_model.LinearRegression()
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05']
    coefRMSETC1, coefRMSETC2 = [[],[],[]], [[],[],[]]
    
    #Picking up force/RMSE and TC error of each sample
    with open(rstfile,'r') as f1:
        RMSETCLC = [[[] for i in range(3)] for j in range(7)]
        RMSETCmix= [[] for i in range(3)]
        dt = csv.reader(f1)
        L1, Lm = 0, 0
        for row in dt:
            gname = re.split('[-]',row[0])
            if gname[1] in grps:
                i=grps.index(gname[1])
                RMSETCLC[i][0].append(float(row[1]))
                RMSETCLC[i][1].append(abs(float(row[2])))
                RMSETCLC[i][2].append(float(row[2]))
                L1=L1+1
            elif gname[1]=="mix":
                RMSETCmix[0].append(float(row[1]))
                RMSETCmix[1].append(abs(float(row[2])))
                RMSETCmix[2].append(float(row[2]))
                Lm=Lm+1
            else:
                print(f'Error: Grpname [{gname[1]}] is not valid.')
                sys.exit()
                
        print(f'({L1})LC7 and ({Lm})mix data are picked up from {rstfile}')

    #Calculate coef, R^2 and corr of each sample
    for RTDT in RMSETCLC:
        RTDT2D1, RTDT2D2= [], []
        RTDTlen=len(RTDT[0])
        for i in range(RTDTlen):
            RTDT2D1.append([RTDT[1][i]])
            RTDT2D2.append([RTDT[2][i]])
        clf.fit(RTDT2D1,RTDT[0])
        coefRMSETC1[0].append(clf.coef_[0])
        R2RT= clf.score(RTDT2D1,RTDT[0])
        coefRMSETC1[1].append(R2RT)
        corrRT= np.corrcoef(RTDT[1],RTDT[0])
        coefRMSETC1[2].append(corrRT[0][1])
        clf.fit(RTDT2D2,RTDT[0])
        coefRMSETC2[0].append(clf.coef_[0])
        R2RT2= clf.score(RTDT2D2,RTDT[0])
        coefRMSETC2[1].append(R2RT2)
        corrRT2= np.corrcoef(RTDT[2],RTDT[0])
        coefRMSETC2[2].append(corrRT2[0][1])
        
    RTDT2D1m, RTDT2D2m= [], []
    RTDTlen=len(RMSETCmix[0])
    for i in range(RTDTlen):
        RTDT2D1m.append([RMSETCmix[1][i]])
        RTDT2D2m.append([RMSETCmix[2][i]])
    clf.fit(RTDT2D1m,RMSETCmix[0])
    coefRMSETC1[0].append(clf.coef_[0])
    R2RT= clf.score(RTDT2D1m,RMSETCmix[0])
    coefRMSETC1[1].append(R2RT)
    corrRT= np.corrcoef(RMSETCmix[1],RMSETCmix[0])
    coefRMSETC1[2].append(corrRT[0][1])
    clf.fit(RTDT2D2m,RMSETCmix[0])
    coefRMSETC2[0].append(clf.coef_[0])
    R2RT2= clf.score(RTDT2D2m,RMSETCmix[0])
    coefRMSETC2[1].append(R2RT2)
    corrRT2= np.corrcoef(RMSETCmix[2],RMSETCmix[0])
    coefRMSETC2[2].append(corrRT2[0][1])
    print(f'Len of coefRMSETC1={len(coefRMSETC1[0])}, coefRMSETC2={len(coefRMSETC2[0])}')

    #Plot coef, R^2 and corr of each sample
    xlb=grps+["mix"]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(xlb,coefRMSETC1[0],color="blue",marker=',',label="Coeff")
    ax1.scatter(xlb,coefRMSETC1[1],color="green",marker=',',label="R^2")
    ax1.scatter(xlb,coefRMSETC1[2],color="red",marker=',',label="Correl")
    ax1.grid(True)
    plt.title(title1)
    plt.rcParams["legend.edgecolor"] ='green'
    ax1.legend(loc='upper right', borderaxespad=0.2)
    pf1=plotfile1+".png"
    plt.savefig(pf1)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(xlb,coefRMSETC2[0],color="blue",marker='o',label="Coeff")
    ax1.scatter(xlb,coefRMSETC2[1],color="green",marker='o',label="R^2")
    ax1.scatter(xlb,coefRMSETC2[2],color="red",marker='o',label="Correl")
    ax1.grid(True)
    ttl=title1+" (org TC err)"
    plt.title(ttl)
    plt.rcParams["legend.edgecolor"] ='green'
    ax1.legend(loc='upper right', borderaxespad=0.2)
    pf2=plotfile1+"-2.png"
    plt.savefig(pf2)
    plt.close()

    #Plot scatter and coef of mix sample
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    plt.title(title2)
    ax1.set_xlabel("TC Err (fm 112.1W/m-K:300K)")
    ax1.set_ylabel("force/RMSE (meV/A)")
    ax1.grid(True)
    ax1.scatter(RMSETCmix[1],RMSETCmix[0],c="blue",marker='.')
    plt.plot(RMSETCmix[1], clf.predict(RTDT2D1m))
    pf3=plotfile2+".png"
    plt.savefig(pf3)
    plt.close()

if __name__ == '__main__':
    rstfile="/home/okugawa/HDNNP/Si-190808/result-LC7/RMSETCdata.csv"
    plotfile1="/home/okugawa/HDNNP/Si-190808/result-LC7/grpplot/coef"
    title1="[Lammps-MD LC7] Regres-Coeff, R^2, Correl"
    plotfile2="/home/okugawa/HDNNP/Si-190808/result-LC7/grpplot/coefmix"
    title2="[Lammps-MD LC7] force/RMSE,TCerr and Regres-Coeff"
    calcplotcoeff(rstfile,plotfile1,title1,plotfile2,title2)

    rstfile="/home/okugawa/HDNNP/Si-190808-md/result-LC7/RMSETCdata.csv"
    plotfile1="/home/okugawa/HDNNP/Si-190808-md/result-LC7/grpplot/coef"
    title1="[AIMD LC7] Regres-Coeff, R^2, Correl"
    plotfile2="/home/okugawa/HDNNP/Si-190808-md/result-LC7/grpplot/coefmix"
    title2="[AIMD LC7] force/RMSE,TCerr and Regres-Coeff"
    calcplotcoeff(rstfile,plotfile1,title1,plotfile2,title2)

    rstfile="/home/okugawa/HDNNP/Si-190808-md/result-LC7n/RMSETCdata.csv"
    plotfile1="/home/okugawa/HDNNP/Si-190808-md/result-LC7n/grpplot/coef"
    title1="[AIMD LC7-prePCA] Regres-Coeff, R^2, Correl"
    plotfile2="/home/okugawa/HDNNP/Si-190808-md/result-LC7n/grpplot/coefmix"
    title2="[AIMD LC7-prePCA] force/RMSE,TCerr and Regres-Coeff"
    calcplotcoeff(rstfile,plotfile1,title1,plotfile2,title2)