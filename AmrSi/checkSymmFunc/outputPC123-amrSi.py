# -*- coding: utf-8 -*-
import numpy as np

"""
This script is for outputting PC1/PC2/PC3 data from preprocd_dataset.npz
of Amorphous samples
"""

def makePC123(dtsetfile, outfile, grpname):
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
    
    with open(outfile, 'w') as f1:
        for dt64 in dataset0:
            for dt in dt64:
                wdt=str(dt[0])+" "+str(dt[1])+" "+str(dt[2])+"\n"
                f1.write(wdt)
                
    print(f'Saved PC1/PC2/PC3 data of {grpname}: Shape= {dim0} x {dim1} x {dim2}')

if __name__ == '__main__': 
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    grps=['315','1000-103040','1500-103040']
    sfgrps=["org","SMZ"]
    rcgrps=["6.0","7.0","7.5"]
    outdir=amrfolder+"/result/PC123/"

    for grp in grps:
        dtsetdir=amrfolder+"amr216/"+grp+"smpl/1/"
        dtsetfile=dtsetdir+"data/AmorphousSi216/preprocd_dataset.npz"
        outfile=outdir+grp+"-PC123.txt"
        makePC123(dtsetfile, outfile, grp)
        
    for sfg in sfgrps:
        dtsetdir=amrfolder+"amr216/1500-103040smpl/SymF/SF/"+sfg+"/1/"
        dtsetfile=dtsetdir+"data/AmorphousSi216/preprocd_dataset.npz"
        outfile=outdir+"1500-103040-"+sfg+"-PC123.txt"
        makePC123(dtsetfile, outfile, sfg)
    
    for rcg in rcgrps:
        dtsetdir=amrfolder+"amr216/1500-103040smpl/SymF/Rc/"+rcg+"/1/"
        dtsetfile=dtsetdir+"data/AmorphousSi216/preprocd_dataset.npz"
        outfile=outdir+"1500-103040-Rc"+rcg+"-PC123.txt"
        makePC123(dtsetfile, outfile, rcg)
           