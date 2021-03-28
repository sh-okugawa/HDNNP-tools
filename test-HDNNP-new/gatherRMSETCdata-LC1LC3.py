# -*- coding: utf-8 -*-
import csv, sys
import ast
from itertools import islice
import matplotlib.pyplot as plt

"""
This script is made to output csv file by gathering 3500smpl's
1) force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
2) train curve data (epoch, trained force/RMSE, validated, difference))
And plot train curve and scatter of force/RMSE&TC data
"""

def gatherRMSETC(LC7folder, datatag):
    #gather force/RMSE & TC data  
    rstfile=LC7folder+"result/RMSETCdata.csv"

    with open(rstfile, 'w') as rslt:
        writer1 = csv.writer(rslt, lineterminator='\n')
        
        for j in range(1, 6):
            dataname=datatag+"-"+str(j)
            datadir= LC7folder+str(j)
            logfile= datadir+"/output/CrystalSi64/training.log"

            with open(logfile, 'r') as log:
                logdata= log.read()
                listdata= ast.literal_eval(logdata)
                listlen= len(listdata)
                for epc in range(9, listlen, 10):
                    vf=float(listdata[epc]["val/main/RMSE/force"])*1000
                
            TCfile =datadir+"/predict-phono3py/out.txt"
            with open(TCfile, 'r') as TCf:
                for n, line in enumerate(TCf):
                    if 'Thermal conductivity (W/m-k)' in line:
                        TCf.seek(0)
                        for lined in islice(TCf, n+32, n+33):
                            data=lined.split()
                            if data[0]!="300.0":
                                print(f'TC read error: [{data[0]}]K data is read')
                                sys.exit()
                            TCerr=abs(float(data[1])-112.1)

            RMSETCdt=[dataname]+[vf]+[TCerr]
            writer1.writerow(RMSETCdt)
            print(f'{dataname} data is gathered and train curve is plotted')    

if __name__ == '__main__': 
    LC3folder="/home/okugawa/test-HDNNP-new/HDNNP/Si-200917/1000K-LC3/mix/3000smpl/"
    LC1folder="/home/okugawa/test-HDNNP-new/HDNNP/Si-200917/1000K-LC1/1500smpl/"

    #gather force/RMSE & TC data of small 
    gatherRMSETC(LC3folder,"LC3mix-3000")
    gatherRMSETC(LC1folder,"LC1.00-1500")