# -*- coding: utf-8 -*-
import csv, sys
import ast
from itertools import islice

"""
This script is made to output csv file by gathering small's
1) force/RMSE of train/validation & TC(300K) diff from 112.1 
"""

if __name__ == '__main__': 
    T5L7folder="/home/okugawa/HDNNP/Si-200917/T5L7/"
    rstfile= T5L7folder+"result/RMSETCdata.csv"
    grps= ["TL3-L7","TL3-L79","TL3-LM3","TM3-L7","TM3-L79","TM3-LM3",
           "TH3-L7","TH3-L79","TH3-LM3","TL2-L7","TML2-L7","TMH2-L7",
           "TH2-L7","TL3-LM5","TM3-LM5","TH3-LM5","all60"]
    
    #gather force/RMSE & TC data  
    with open(rstfile, 'w') as rslt:
        writer1 = csv.writer(rslt, lineterminator='\n')

        for grp in grps:
            for j in range(1, 11):
                dataname=grp+"-"+str(j)
                datadir= T5L7folder+grp+"/"+str(j)

                logfile= datadir+"/output/CrystalSi64/training.log"
                with open(logfile, 'r') as log:
                    logdata= log.read()
                    listdata= ast.literal_eval(logdata)
                    vf=float(listdata[-1]["val/main/RMSE/force"])*1000
                    
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
            print(f'force/RMSE & TC data of /T5L7/{grp} is gathered')