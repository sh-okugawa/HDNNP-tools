# -*- coding: utf-8 -*-
import os
import shutil

"""
This script is for copying 3 files of /predict-phono3py folder to
/predict-phono3py-2 folder in order to run phono3py again by 
new prediction_application.py which is added saving symm_func to npz file
"""

def fileEdit(datadir):
    copiedfile=['POSCAR-unitcell','phono3pyPrep.py','phono3pyRun.py']
    
    os.makedirs(datadir+"/predict-phono3py-2")
    dirorg = datadir+"/predict-phono3py/"
    dirdest = datadir+"/predict-phono3py-2"

    for cpf in copiedfile:
        shutil.copy2(dirorg+cpf, dirdest)
           
if __name__ == '__main__': 
    root="/home/okugawa/HDNNP/Si-190808/1000K-LC7/"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
        
    for grp in grps:
        for i in range(1, 11):
            if grp=='mix':
                for j in range(1, 11):
                    datadir=root+grp+"/"+str(i)+"/"+str(j)
                    fileEdit(datadir)
                    
            else:
                datadir=root+grp+"/"+str(i)
                fileEdit(datadir)

        print(f'Copied phono3py-2 of /1000K-LC7/{grp}')