# -*- coding: utf-8 -*-
import csv
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

"""
This script is for calculating Linear-Regression and correlation of
force/RMSE and TC by sklearn linear-model 
"""

def calcoeff(rstfile):
    clf = linear_model.LinearRegression()
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05']
    coefRMSETC, coefRMSETCmix = [], []
    
    #Picking up force/RMSE and TC error of each sample
    with open(rstfile,'r') as f1:
        RMSETCLC = [[[] for i in range(3)] for j in range(8)]
        RMSETCmix= [[[] for i in range(3)] for j in range(10)]
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
                i=int(gname[2])-1
                RMSETCmix[i][0].append(float(row[1]))
                RMSETCmix[i][1].append(abs(float(row[2])))
                RMSETCmix[i][2].append(float(row[2]))
                Lm=Lm+1
                if gname[3]=="1":
                    RMSETCLC[7][0].append(float(row[1]))
                    RMSETCLC[7][1].append(abs(float(row[2])))
                    RMSETCLC[7][2].append(float(row[2]))
                    L1=L1+1
            else:
                print(f'Error: Grpname [{gname[1]}] is not valid.')
                sys.exit()
                
        print(f'({L1})LC7 and ({Lm})mix data are picked up from {rstfile}')
               
    for i,RTDT in enumerate(RMSETCLC):
        RTDT2D1, RTDT2D2= [], []
        RTDTlen=len(RTDT[0])
        for i in range(RTDTlen):
            RTDT2D1.append([RTDT[1][i]])
            RTDT2D2.append([RTDT[2][i]])
        clf.fit(RTDT2D1,RTDT[0])
        coefRT= list(clf.coef_)
        R2RT= clf.score(RTDT2D1,RTDT[0])
        corrRT= np.corrcoef(RTDT[1],RTDT[0])
        coefRT.append(R2RT)
        coefRT.append(corrRT[0][1])
        coefRMSETC.append(coefRT)
        clf.fit(RTDT2D2,RTDT[0])
        coefRT= list(clf.coef_)
        R2RT= clf.score(RTDT2D2,RTDT[0])
        corrRT= np.corrcoef(RTDT[2],RTDT[0])
        coefRT.append(R2RT)
        coefRT.append(corrRT[0][1])
        coefRMSETC.append(coefRT)
        
    for i,RTDT in enumerate(RMSETCmix):
        RTDT2D1, RTDT2D2= [], []
        RTDTlen=len(RTDT[0])
        for i in range(RTDTlen):
            RTDT2D1.append([RTDT[1][i]])
            RTDT2D2.append([RTDT[2][i]])
        clf.fit(RTDT2D1,RTDT[0])
        coefRT= list(clf.coef_)
        R2RT= clf.score(RTDT2D1,RTDT[0])
        corrRT= np.corrcoef(RTDT[1],RTDT[0])
        coefRT.append(R2RT)
        coefRT.append(corrRT[0][1])
        coefRMSETCmix.append(coefRT)
        clf.fit(RTDT2D2,RTDT[0])
        coefRT= list(clf.coef_)
        R2RT= clf.score(RTDT2D2,RTDT[0])
        corrRT= np.corrcoef(RTDT[2],RTDT[0])
        coefRT.append(R2RT)
        coefRT.append(corrRT[0][1])
        coefRMSETCmix.append(coefRT)
        
    print(f'Len of coefRMSETC={len(coefRMSETC)}, coefRMSETCmix={len(coefRMSETCmix)}')
    return([coefRMSETC, coefRMSETCmix])

if __name__ == '__main__':
    rstfile="/home/okugawa/HDNNP/Si-190808/result-LC7/RMSETCdata.csv"
    coefRT=calcoeff(rstfile)
    print(f'coefRMSETC of Lammps-MD LC7:\n')
    print(coefRT[0])
    print(f'coefRMSETC of Lammps-MD LC7mix:\n')
    print(coefRT[1])
    print(f'\n')

    rstfile="/home/okugawa/HDNNP/Si-190808-md/result-LC7/RMSETCdata.csv"
    coefRT=calcoeff(rstfile)
    print(f'coefRMSETC of AIMD LC7:\n')
    print(coefRT[0])
    print(f'coefRMSETC of AIMD LC7-mix:\n')
    print(coefRT[1])
    print(f'\n')

    rstfile="/home/okugawa/HDNNP/Si-190808-md/result-LC7n/RMSETCdata.csv"
    coefRT=calcoeff(rstfile)
    print(f'coefRMSETC of AIMD LC7n:\n')
    print(coefRT[0])
    print(f'coefRMSETC of AIMD LC7n-mix:\n')
    print(coefRT[1])