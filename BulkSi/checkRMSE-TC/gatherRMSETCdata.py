# -*- coding: utf-8 -*-
import os
import csv
import ast
from itertools import islice

"""
This script is made to output csv file by gathering 
force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
from all RMSE data and TC data
"""

if __name__ == '__main__': 
    root=os.getcwd()

    tdata=["2","5","10","20","40","60","80","100"]
    node=["50","100","200","300","500"]
    rstfile=root+"/result/RMSETCdata.csv"
    
    with open(rstfile, 'w') as rslt:
        writer1 = csv.writer(rslt, lineterminator='\n')
        for k in tdata:
            for i in node:
                for j in range(1, 11):
                    logfile= root+"/d"+k+"n"+i+"/"+str(j)+"/output/CrystalSi64/training.log"
                    dataname= "d"+k+"n"+i+"-"+str(j)

                    with open(logfile, 'r') as log:
                        logdata= log.read()
                        listdata= ast.literal_eval(logdata)
                        listlen= len(listdata)
                        diffnum=0
                        difftotal=0
                        for epc in range(9, listlen, 10):
                            vf=float(listdata[epc]["val/main/RMSE/force"])*1000
                    
                    infile =root+"/d"+k+"n"+i+"/"+str(j)+"/predict-phono3py/out.txt"
                    with open(infile, 'r') as infl:
                        for n, line in enumerate(infl):
                            if 'Thermal conductivity (W/m-k)' in line:
                                infl.seek(0)
                                for lined in islice(infl, n+32, n+33):
                                     data=lined.split()
                                     TCerr=float(data[1])-112.1

                    RMSEdt=[dataname]+[vf]+[TCerr]
                    writer1.writerow(RMSEdt)

