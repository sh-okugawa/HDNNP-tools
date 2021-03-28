# -*- coding: utf-8 -*-
import sys
import numpy as np  # Numerical array library
import random

"""
This script is for picking up force data from vasp result and also 
 derivative data (1st differentiate of symm_func) from symmetry_function.npz, 
 then calculate Ridge regression of both and plot its result
 [for Amorphous Si 315smpl]
"""

    
if __name__ == '__main__': 
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    amrfolder2="/home/okugawa/test-HDNNP-new/HDNNP/Si-amr/amr216/"
    forcefolder=amrfolder+"datas/force/"
    forcefile=forcefolder+"amrsi-315f.txt"
    SFfile=amrfolder2+"315smpl/1/data/AmorphousSi216/symmetry_function.npz"
    smpls=[i for i in range(315)]
    atms=[i for i in range(216)]
    sfs=[i for i in range(48)]

    # Read derivative data ([smpl]x[atom]x[symm_func]x[diff] : 4-dim) from 
    #  symmetry_function.npz and reshape & split to
    #  [smpl x atom]x[sym_func x diffx], [smpl x atom]x[sym_func x diffy], 
    #  [smpl x atom]x[sym_func x diffz] : (2-dim)x3
    symt= np.load(SFfile)
    dervdt= symt['derivative']
    dL0=len(dervdt)
    dL1=len(dervdt[0])
    dL2=len(dervdt[0][0])
    dL3=len(dervdt[0][0][0])
    print(f'Derivative shape = {dL0}x{dL1}x{dL2}x{dL3}')
    dLatom=dL0*dL1
    
    if dL3/3 != dL1:
        print(f'Derivative shape error: {dL3} is not {dL1}x3')
        sys.exit()
    
    #Reshape derivative array from [smpl]x[atom]x[symm_func]x[diff] (4-dim) to
    # [smpl x atom]x[sym_func]x[diff] (3-dim),  ([diff] should be [atom]x3)
    dervrsp1=dervdt.reshape(dLatom,dL2,dL3)
    # then reshape [diff] to [3]x[diffx/y/z]  => [smpl x atom]x[sym_func]x[3]x[diffx/y/z] (4-dim),
    dervrsp2=dervrsp1.reshape([dLatom,dL2,3,dL1], order='F')
    # then finally reshape to [smpl x atom]x[sym_func x diffx/y/z] (2-dim)x3
    diffx,diffy,diffz=[],[],[]
    difxx,difyy,difzz=[],[],[]
    for dsmpl in dervrsp2:
        for dsymf in dsmpl:  #dsymf has [3]x[diffx/y/z] shape
            difxx.extend(dsymf[0])
            difyy.extend(dsymf[1])
            difzz.extend(dsymf[2])
        diffx.append(difxx)
        diffy.append(difyy)
        diffz.append(difzz)
        difxx,difyy,difzz=[],[],[]
    diffxyz=[np.array(diffx),np.array(diffy),np.array(diffz)]
    print('Derivative data is read from symmetry_function.npz')
    
    #Check reshape is correctly done or not
    for nn in range(100):
        smplnum=random.choice(smpls)
        atmnum=random.sample(atms,2)
        sfnum=random.choice(sfs)
        
        orgx=dervdt[smplnum][atmnum[0]][sfnum][atmnum[1]*3]
        orgy=dervdt[smplnum][atmnum[0]][sfnum][atmnum[1]*3+1]
        orgz=dervdt[smplnum][atmnum[0]][sfnum][atmnum[1]*3+2]
        
        respx=diffx[smplnum*216+atmnum[0]][sfnum*216+atmnum[1]]
        respy=diffy[smplnum*216+atmnum[0]][sfnum*216+atmnum[1]]
        respz=diffz[smplnum*216+atmnum[0]][sfnum*216+atmnum[1]]

        if orgx==respx and orgy==respy and orgz==respz:
            rslt='OK'
        else:
            rslt='NG'
        print(f'{rslt} {smplnum} {atmnum[0]} {sfnum} {atmnum[1]}: {orgx} {respx} {orgy} {respy} {orgz} {respz}')
