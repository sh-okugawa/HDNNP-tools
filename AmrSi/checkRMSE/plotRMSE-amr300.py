# coding: utf-8
import matplotlib.pyplot as plt

"""
This script is for gathering force/RMSE data from training result of
Si-amorphous with sample20.xyz data for 40/100/200 node & 2/3/4/5 layer
and plot them
"""

if __name__ == '__main__': 
    amr300folder= "/home/okugawa/HDNNP/Si-amr/amr216/300smpl/"
    plotfile= "/home/okugawa/HDNNP/Si-amr/result/300smpl/grpplot/amr300-fRMSE.png" 
    
    colors= ["red","orange","lime","b"]
    nodes= ["40","100","200"]
    lbls, clrs= [], []
    FRs= [[] for i in range(5)]
    
    for node in nodes:
        for layer in range(2, 6):
            lbl= node+"-"+str(layer)
            for i in range(1, 6):
                wkfolder= amr300folder+lbl+"/"+str(i)
                stdoutfile= wkfolder+"/stdout"
                with open(stdoutfile, 'r') as outf:
                    datas= outf.readlines()
                    lastline= datas[-1]
                    if "early stopping" in lastline:
                        lastline= datas[-2]
                    FR= lastline.split()[6]
                    FRs[i-1].append(float(FR)*1000)
            lbls.append(lbl)
            clrs.append(colors[layer-2])

    #Plot force/RMSE of each group 
    fig = plt.figure(figsize=(8, 5))
    ax1 = fig.add_subplot(111)
    plttitle="force/RMSE of 2/3/4/5 H-layers with 20/100/200 nodes"
    plt.title(plttitle)
    ax1.set_ylabel("force/RMSE (meV/ang)", fontsize=10)
    ax1.set_xlabel("node#-layer#", fontsize=10)
    plt.xticks(fontsize=10)  #Font size of x-axis scale            
    ax1.grid(True)
    plt.rcParams["legend.edgecolor"] ='green'
    plt.rcParams["legend.facecolor"] ='white'
    plt.rcParams["legend.framealpha"] ='1'
              
    for i in range(5):
        ax1.scatter(lbls, FRs[i], c=clrs, marker='.')

    #ax2 is only for plotting legend of all kind of data
    ax2 = ax1.twinx()
    for k in range(4):
        ax2.scatter(lbls,FRs[k],c=colors[k],marker='.',label=str(k+2)+" layers")
    handler2, label2 = ax2.get_legend_handles_labels()
    ax1.legend(handler2, label2,loc='upper left',title='Hidden layer',)
    fig.delaxes(ax2)
    plt.savefig(plotfile)
    print(f'force/RMSE data of amr-300smpl is plotted')
    plt.close()