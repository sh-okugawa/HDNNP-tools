# -*- coding: utf-8 -*-
import ast
import csv

"""
This script is for gathering force/RMSE of /small
 and saving to csv
"""
            
if __name__ == '__main__':
    smallfolder="/home/okugawa/test-HDNNP-new/HDNNP/Si-200917/small/"
    rstfile=smallfolder+"result/RMSEdata.csv"
    
    #Read force/RMSE data from log file
    with open(rstfile, 'w') as rst:
        writer2 = csv.writer(rst, lineterminator='\n')
            
        for i in range(1,21):
            logfile=smallfolder+str(i)+"/output/CrystalSi64/training.log"
            dataname="small-"+str(i)
            with open(logfile, 'r') as log:
                logdata= log.read()
                listdata= ast.literal_eval(logdata)
                ve=float(listdata[-1]["val/main/RMSE/energy"])*1000
                vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                vt=float(listdata[-1]["val/main/total"])*1000
                outdata=[dataname]+[ve]+[vf]+[vt]
                writer2.writerow(outdata)