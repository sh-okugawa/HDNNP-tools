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

def gatherRMSETC(LC7folder,rstfolder):
    #gather force/RMSE & TC data  
    rstfile=rstfolder+"RMSETCdata.csv"
    traindir=rstfolder+"traincv/"

    with open(rstfile, 'w') as rslt:
        writer1 = csv.writer(rslt, lineterminator='\n')
        
        for j in range(1, 11):
            dataname="LC7mix-3500-"+str(j)
            datadir= LC7folder+str(j)
            logfile= datadir+"/output/CrystalSi64/training.log"
            traincvfile= traindir+dataname+".csv"
            plotfile= traindir+"plot/"+dataname+".png"

            with open(logfile, 'r') as log:
                logdata= log.read()
                listdata= ast.literal_eval(logdata)
                listlen= len(listdata)
                epl=[]
                tfl=[]
                vfl=[]
                diffl=[]
                with open(traincvfile, 'w') as tcv:
                    writer2 = csv.writer(tcv, lineterminator='\n')
                    for epc in range(9, listlen, 10):
                        ep=int(listdata[epc]["epoch"])
                        tf=float(listdata[epc]["main/RMSE/force"])*1000
                        vf=float(listdata[epc]["val/main/RMSE/force"])*1000
                        diff=vf-tf
                        outdata=[ep]+[tf]+[vf]+[diff]
                        writer2.writerow(outdata)
                        epl.append(ep)
                        tfl.append(tf)
                        vfl.append(vf)
                        diffl.append(diff)
                            
                # Plotting Training curve and diff of Train&Validation
                # Axis-1: ax1 for Train and Validation
                # Axis-2: ax2 for difference of Train and Validation
                fig = plt.figure()
                ax1 = fig.add_subplot(111)
                ln1 = ax1.plot(epl, tfl, color="blue", label="Train")
                ln2 = ax1.plot(epl, vfl, color="red", label="Validation")
                ax2 = ax1.twinx()  # convining ax1 and ax2
                ln3 = ax2.plot(epl, diffl, color="green", label="Diff")
                ax2.set_ylim(-28, 22)  # fixing y-axis scale 
                plt.title(dataname)
                ax1.set_xlabel('epoch')
                ax1.set_ylabel('force/RMSE (meV/ang)')
                ax1.grid(True)
                ax2.set_ylabel('Diff (Val-Trn)')
                # merging legend of ax1 and ax2
                handler1, label1 = ax1.get_legend_handles_labels()
                handler2, label2 = ax2.get_legend_handles_labels()
                ax1.legend(handler1 + handler2, label1 + label2, loc=2)
                plt.savefig(plotfile)
                plt.close()
                
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
    LC7folder="/home/okugawa/test-HDNNP-new/HDNNP/Si-200917/1000K-LC7/mix/3500smpl/"

    #gather force/RMSE & TC data of small 
    rstfolder= LC7folder+"result/"
    gatherRMSETC(LC7folder,rstfolder)