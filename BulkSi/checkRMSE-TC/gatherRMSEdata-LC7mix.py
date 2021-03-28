# -*- coding: utf-8 -*-
import ast
import csv

"""
This script is for gathering force/RMSE of /1000K-LC7/mix/3500smpl
 and saving to csv
"""
            
if __name__ == '__main__':
    mixfolder="/home/okugawa/HDNNP/Si-200917/1000K-LC7/mix/"
    rstfile=mixfolder+"result/RMSEdata-3500smpl.csv"
    
    #Read force/RMSE data from log file
    with open(rstfile, 'w') as rst:
        writer2 = csv.writer(rst, lineterminator='\n')
            
        for i in range(1,31):
            logfile=mixfolder+"3500smpl/"+str(i)+"/output/CrystalSi64/training.log"
            dataname="3500mix-"+str(i)
            with open(logfile, 'r') as log:
                logdata= log.read()
                listdata= ast.literal_eval(logdata)
                vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                outdata=[dataname]+[vf]
                writer2.writerow(outdata)