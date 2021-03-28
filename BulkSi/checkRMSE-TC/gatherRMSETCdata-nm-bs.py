# -*- coding: utf-8 -*-
import os
import csv
import ast
from itertools import islice
import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy

"""
This script is made to output csv file by gathering 
1) force/RMSE & difference of train/validation & TC(300K) diff from 112.1 
2) train curve data (epoch, trained force/RMSE, validated, difference))
from RMSE/TC data of bad samples (8kindx700samplesx10times with node=50)
And plot out each data with classified color by normalized distance
"""

def fileEdit(fname, data, k):
    with open(fname, 'r') as f1:
        tmp_list =[]
        i=0
        for line in f1:
            tmp_list.append(line.rstrip()+","+str(data[i][k])+"\n")
            i=i+1

    with open(fname, 'w') as f2:
        for i in range(len(tmp_list)):
            f2.write(tmp_list[i])

if __name__ == '__main__': 
    root=os.getcwd()

    bsxs=["bs1","bs2","bs3","bs4","bs5","bs6","bs7","bs8"]

    rstfile=root+"/result/RMSEdata.csv"
    os.makedirs(root+"/result/traincv/plot")
    os.makedirs(root+"/result/grpplot")
    traindir=root+"/result/traincv/"
    plotdir=root+"/result/grpplot/"
    labels=('nrm>0.9','0.9>nrm>0.6','0.6>nrm>0.4','0.4>nrm>0.2','0.2>nrm>0.1','0.1>nrm')
    colors=("red","orange","yellow","cyan","c","b")
    
    with open(rstfile, 'w') as rslt:
        writer1 = csv.writer(rslt, lineterminator='\n')
        RMSETC = []
        
        for bsx in bsxs:
            grpname=bsx
            print(grpname+" data gathering")
            vfp=[]
            TCerrp=[]
                
            for j in range(1, 11):
                dataname=grpname+"-"+str(j)
                datadir= root+"/"+grpname+"-d20n50/"+str(j)
                logfile= datadir+"/output/CrystalSi64/training.log"
                traincvfile= traindir+dataname+".csv"
                plotfile= traindir+"/plot/"+dataname+".png"

                with open(logfile, 'r') as log:
                    logdata= log.read()
                    listdata= ast.literal_eval(logdata)
                    listlen= len(listdata)
                    diffnum=0
                    difftotal=0
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
                    ax1.set_ylabel('force/RMSE (meV/A)')
                    ax1.grid(True)
                    ax2.set_ylabel('Diff (Val-Trn)')
                    # merging legend of ax1 and ax2
                    handler1, label1 = ax1.get_legend_handles_labels()
                    handler2, label2 = ax2.get_legend_handles_labels()
                    ax1.legend(handler1 + handler2, label1 + label2, loc=2)
                    plt.savefig(plotfile)
                    plt.close()
                    
                infile =datadir+"/predict-phono3py/out.txt"
                with open(infile, 'r') as infl:
                    for n, line in enumerate(infl):
                        if 'Thermal conductivity (W/m-k)' in line:
                            infl.seek(0)
                            for lined in islice(infl, n+32, n+33):
                                data=lined.split()
                                TCerr=abs(float(data[1])-112.1)

                RMSEdt=[dataname]+[vf]+[TCerr]
                writer1.writerow(RMSEdt)
                vfp.append(vf)
                TCerrp.append(TCerr)
                RMSETC.append([vf,TCerr])

    #Calculation normalized value of force/RMSE and TC error
    print("Calculating normalized value of force/RMSE and TC error")
    mm = preprocessing.MinMaxScaler()
    nrmp= mm.fit_transform(RMSETC)
    dtn=0
    normll=[]
    nrmhist=[]
    for bsx in bsxs:
        for j in range(1, 11):
            normalized= numpy.sqrt((nrmp[dtn][0]**2)+(nrmp[dtn][1]**2))
            if normalized>0.9:
                normll.append([colors[0],normalized])
            elif normalized>0.6:
                normll.append([colors[1],normalized])
            elif normalized>0.4:
                normll.append([colors[2],normalized])
            elif normalized>0.2:
                normll.append([colors[3],normalized])
            elif normalized>0.1:
                normll.append([colors[4],normalized])
            else:
                normll.append([colors[5],normalized])
            nrmhist.append(normalized)
            dtn=dtn+1
    fileEdit(rstfile, normll, 1)
                   
    #Plotting correlation of force/RMSE and TC error for each group
    print("Plotting colleration of each group and all data")
    dtn=0
    for bsx in bsxs:
        grpname=bsx
        grpplotfile=plotdir+grpname+".png"
            
        fig = plt.figure()
        ax3 = fig.add_subplot(111)
        plt.title(grpname)
        ax3.set_xlabel("TC Err (fm 112.1)")
        ax3.set_ylabel("force/RMSE (meV/A)")
        ax3.grid(True)
        plt.rcParams["legend.edgecolor"] ='green'
            
        for j in range(0, 10):
            ax3.scatter(RMSETC[dtn][1],RMSETC[dtn][0],c=normll[dtn][0],marker='o')
            dtn=dtn+1

        left, right = ax3.get_xlim()
        ax3.set_xlim(-0.1, right*1.2)
        #ax4 is only for plotting legend of all kind of data
        ax4 = ax3.twinx()
        for j in range(0, 6):
            lbl=labels[j]
            clr=colors[j]
            ax4.scatter(RMSETC[dtn-1][1],RMSETC[dtn-1][0],c=clr,marker='o',label=lbl)
        handler4, label4 = ax4.get_legend_handles_labels()
        ax3.legend(handler4, label4,loc='upper right',title='Normalized',bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
        fig.delaxes(ax4)
        plt.savefig(grpplotfile)
        plt.close()
 
    #Plotting all data of correlation of force/RMSE and TC error
    dtn=0
    allplotfile=plotdir+"alldata.png"
    fig = plt.figure()
    ax3 = fig.add_subplot(111)
    plt.title("All data")
    ax3.set_xlabel("TC Err (fm 112.1)")
    ax3.set_ylabel("force/RMSE (meV/A)")
    ax3.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
                
    for bsx in bsxs:
        for j in range(0, 10):
            ax3.scatter(RMSETC[dtn][1],RMSETC[dtn][0],c=normll[dtn][0],marker='.')
            dtn=dtn+1

    left, right = ax3.get_xlim()
    ax3.set_xlim(-0.1, right*1.2)
    #ax4 is only for plotting legend of all kind of data
    ax4 = ax3.twinx()
    for j in range(0, 6):
        lbl=labels[j]
        clr=colors[j]
        ax4.scatter(RMSETC[0][1],RMSETC[0][0],c=clr,marker='.',label=lbl)
    handler4, label4 = ax4.get_legend_handles_labels()
    ax3.legend(handler4, label4,loc='upper right',title='Normalized',bbox_to_anchor=(0.97, 0.85, 0.14, .100),borderaxespad=0.,)
    fig.delaxes(ax4)
    plt.savefig(allplotfile)
    plt.close()
    
    #Plotting histgram of normalized data
    histplotfile=plotdir+"histnrm.png"
    fig = plt.figure()
    ax5 = fig.add_subplot(111)
    ax5.hist(nrmhist, bins=15)
    ax5.set_title("Histgram of normalized data")
    ax5.set_ylabel("Frequency")
    ax5.set_xlabel("Normalized data")
    plt.savefig(histplotfile)
    plt.close()
        
