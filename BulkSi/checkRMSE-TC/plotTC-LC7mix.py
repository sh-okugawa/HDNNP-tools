# coding: utf-8
import matplotlib.pyplot as plt
import csv
from itertools import islice

"""
This script is for gathering Thermal conductivity data of Si 1000K-LC7mix
"""

if __name__ == '__main__': 
    LC7folder="/home/okugawa/HDNNP/Si-200917/1000K-LC7/"
    grps=["mix"]

    TCcvdir=LC7folder+"result/TCcv/"
    plotdir=LC7folder+"result/grpplot/"
    
    #Read TC of Si 1000K-LC7-mix data from /predict-phono3py/out.txt
    TCdt=[[[],[]] for i in range(20)]
    for grp in grps:
        for i in range(1,21):
            grpname=grp+"-"+str(i)
            TCfile =LC7folder+grp+"/"+str(i)+"/predict-phono3py/out.txt"
            TCdtfile=TCcvdir+"TCdata/"+grpname+".csv"
        
            with open(TCfile, 'r') as TCf, open(TCdtfile, 'w') as TCdtf:
                writer2 = csv.writer(TCdtf, lineterminator='\n')
                for n, line in enumerate(TCf):
                    if 'Thermal conductivity (W/m-k)' in line:
                        TCf.seek(0)
                        lenSMZ=0
                        for lined in islice(TCf, n+3, n+103):
                            data=lined.split()
                            wrdata=[float(data[0]),float(data[1]),float(data[2]),float(data[3])]
                            writer2.writerow(wrdata)
                            TCdt[i-1][0].append(float(data[0]))
                            TCdt[i-1][1].append(float(data[1]))
                            lenSMZ+=1
                        break
            print(f'{grpname} TC data ({lenSMZ}) was read')
                    
    #Plot TC curve of each sample
    for grp in grps:
        for i in range(20):
            grpname=grp+"-"+str(i+1)
            plotfile=TCcvdir+grpname+".png"
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            plt.title(f'[Si 1000K-LC7 {grpname}] Thermal Conductivity')
            ax1.set_xlabel("Temperature (K)")
            ax1.set_ylabel("Thermal Conductivity (W/m-K)")
            ax1.grid(True)
            ax1.set_ylim(0, 700)
            ax1.plot(TCdt[i][0],TCdt[i][1],c="black")
            plt.savefig(plotfile)
            plt.close()