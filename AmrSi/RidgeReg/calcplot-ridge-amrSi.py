# -*- coding: utf-8 -*-
import sys
import numpy as np  # Numerical array library
import matplotlib.pyplot as plt  # Plotting
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

"""
This script is for picking up force data from vasp result and also 
 derivative data (1st differentiate of symm_func) from symmetry_function.npz, 
 then calculate Ridge regression of both and plot its result
 [for Amorphous Si 315smpl]
"""

def readderivative(SFfile):
# Read derivative data ([smpl]x[atom index]x[symm_func]x[xyz of diff index] : 4-dim) 
#  from symmetry_function.npz and pick up x/y/z of diff index which is
#  corresponding to atom index
    symt= np.load(SFfile)
    dervdt= symt['derivative']
    dL0=len(dervdt)
    dL1=len(dervdt[0])
    dL2=len(dervdt[0][0])
    dL3=len(dervdt[0][0][0])
    
    if dL3/3 != dL1:
        print(f'Derivative shape error: {dL3} is not {dL1}x3')
        sys.exit()
    
    #Reshape derivative array from
    # [smpl]x[atom index]x[symm_func]x[xyz of diff index] (4-dim) to
    # [smpl]x[atom index]x[sym_func]x[3(x/y/z)]x[diff index] (5-dim)
    # **[xyz of diff index] should be [atom index]x3)
    dervrsp=dervdt.reshape([dL0,dL1,dL2,3,-1], order='F')

    datax,datay,dataz=[],[],[]
    for ddd in dervrsp:                 #for each smpl
        for atom,dd in enumerate(ddd):  #for each atom index
            ddx,ddy,ddz=[],[],[]
            for d in dd:  # for each symm_func
                ddx.append(d[0][atom]) #pick up x of diff index which corresponding to atom index
                ddy.append(d[1][atom]) #pick up y of diff index which corresponding to atom index
                ddz.append(d[2][atom]) #pick up z of diff index which corresponding to atom index
            datax.append(ddx)
            datay.append(ddy)
            dataz.append(ddz)

    datax_array=np.array(datax)
    datay_array=np.array(datay)
    dataz_array=np.array(dataz)
    diffxyz=[datax_array,datay_array,dataz_array]

    print(f'Shape transfer:{dervdt.shape} => {dervrsp.shape} => {datax_array.shape}x3')
    print('Derivative data is read from symmetry_function.npz')
    return(diffxyz)
    
if __name__ == '__main__': 
    amrfolder="/home/okugawa/HDNNP/Si-amr/"
    amrfolder2="/home/okugawa/test-HDNNP-new/HDNNP/Si-amr/amr216/"
    forcefolder=amrfolder+"datas/force/"
    forcefile=forcefolder+"amrsi-315f.txt"
    SFfile=amrfolder2+"315smpl/1/data/AmorphousSi216/symmetry_function.npz"
    xyzgrp=['x','y','z']
    RdgAlpha=[1,10]
    test_ratio=0.2

    #Read fx/fy/fz of vasp result and set as response variable for Ridge regression
    fx,fy,fz=[],[],[]
    with open(forcefile, 'r') as f1:
        fclist=[]
        for line in f1:
            linesp=line.split()
            fx.append(float(linesp[0]))
            fy.append(float(linesp[1]))
            fz.append(float(linesp[2]))
    frcxyz=[np.array(fx),np.array(fy),np.array(fz)]
    print('fx/fy/fz of vasp result is read')

    #Read predictor vector from derivative data in symmetry_function.npz
    diffxyz=readderivative(SFfile)
    diffxL=len(diffxyz[0])
    diffyL=len(diffxyz[1])
    diffzL=len(diffxyz[2])
    
    if diffxL!=len(fx) or diffyL!=len(fy) or diffzL!=len(fz):
        errx='Len of diffx='+str(diffxL)+' : fx='+str(len(fx))+'\n'
        erry='Len of diffy='+str(diffyL)+' : fy='+str(len(fy))+'\n'
        errz='Len of diffz='+str(diffzL)+' : fz='+str(len(fz))
        print('Data length error: \n'+errx+erry+errz)
        sys.exit()
        
    #Ridge regression for fx,fy,fz
    for xyznum,dfxyz in enumerate(diffxyz):
        fxyz=frcxyz[xyznum]
        print(f'Shape of diff{xyzgrp[xyznum]}={dfxyz.shape} f{xyzgrp[xyznum]}={len(fxyz)}')
        X_train, X_test, y_train, y_test = train_test_split(dfxyz, fxyz, test_size=test_ratio)

        for alp in RdgAlpha:
            ridge_reg=Ridge(alpha=alp, solver="cholesky")
            ridge_reg.fit(X_train,y_train)
            predict=ridge_reg.predict(X_test)
            MSE=mean_squared_error(predict,y_test)
            RMSE=' RMSE='+str(round(np.sqrt(MSE),4))
            trainscore=ridge_reg.score(X_train, y_train)
            testscore=ridge_reg.score(X_test, y_test)
            print(f'MSE={MSE}')
            plttext=RMSE+'\n TrainScore='+str(trainscore)+'\n TestScore='+str(testscore)
            plt.axes().set_aspect('equal')
            plt.scatter(predict,y_test, marker='.')
            frcname='force-'+xyzgrp[xyznum]+"-a"+str(alp)
            plt.title('[Amorphous Si 315smpl] Ridge regression of '+frcname)
            plt.text(0.8, 0.75, plttext)
            plt.savefig(forcefolder+"Ridge_reg_"+frcname+".png")
            plt.close()