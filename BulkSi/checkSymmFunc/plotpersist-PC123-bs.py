# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np
import homcloud.interface as hc
import homcloud.paraview_interface as pv

"""
This script is for plotting persistent diagram of PC1&PC2&PC3
which is loaded from preprocd_dataset.npz of all bs samples
"""

def PlotPersist(dtsetfile, plotdir, grpname):
    dtset= np.load(dtsetfile, allow_pickle=True)
    #allow_pickle op is for adapting spec change of numpy 1.16.3 and later
    dts= dtset['dataset']
    dataset0=[]

    for dt in dts:
        dt0=dt['inputs/0']
        dataset0.append(dt0)

    dim0=len(dataset0)
    dim1=len(dataset0[0])
    dim2=len(dataset0[0][0])
    
    PCdata=[]
    for dt64 in dataset0:
        for dt in dt64:
            PCdata.append([dt[0],dt[1],dt[2]])

    #Plot persistent diagram
    hc.PDList.from_alpha_filtration(PCdata,
                                save_to="pointcloud.idiagram",
                                save_boundary_map=True)
    pdlist = hc.PDList("pointcloud.idiagram")
    pd = pdlist.dth_diagram(1)
    pd.histogram().plot(colorbar={"type": "log"})
    plotfile1=plotdir+grpname+"-pers.png"
    plt.savefig(plotfile1)
    plt.close()
    
    print(f'Plot PC1/PC2/PC3 data of {grpname}: Shape= {dim0} x {dim1} x {dim2}')

if __name__ == '__main__': 
    root=os.getcwd()
    bsxs=["bs1","bs2","bs3","bs4","bs5","bs6","bs7","bs8"]
    plotdir=root+"/result/Persistent/"

    bsx=bsxs[0]
    j=1
    grpname=bsx+"-"+str(j)
    dtsetdir=root+"/"+bsx+"-d20n50/"+str(j)
    dtsetfile=dtsetdir+"/data/CrystalSi64/preprocd_dataset.npz"
    PlotPersist(dtsetfile, plotdir, grpname)