# coding: utf-8
import random
import sys, os
import shutil

"""
This script is for picking up mixed 700 samples randomly from
5000 xyz data of 1000K LC=0.99,1.0,1.01 got by MD
"""

## Modifying output directory name of phonopyPrep.py and phono3pyPrep.py
def fileEdit2(fname, wkfolder):
    index= 'nnpout='
    text= "nnpout='"+wkfolder+"/output'\n"

    with open(fname, 'r') as infl:
        tmp_list =[]
        for row in infl:
            if row.find(index) != -1:
                tmp_list.append(text)
            else:
                tmp_list.append(row)

    with open(fname, 'w') as f2:
        for ii in range(len(tmp_list)):
            f2.write(tmp_list[ii])
  
if __name__ == '__main__': 
    mdfolder="/home/okugawa/HDNNP/Si-190808-md/"
    LC7folder=mdfolder+"1000K-LC7/"
    fldname='mix'
                            
    #create data folders
    dirorgin = mdfolder+"base/predict-phono3py"
    for i in range(1,11):
        for j in range(1,11):
            wkfolder=LC7folder+fldname+"/"+str(i)+"/"+str(j)
            wkfolder3=wkfolder+"/predict-phono3py"
            shutil.rmtree(wkfolder3)       
            shutil.copytree(dirorgin, wkfolder3)
            fname2 = wkfolder3+"/phono3pyPrep.py"
            fileEdit2(fname2, wkfolder)
            
        print(f'Create /1000K-LC7/{fldname}/{str(i)} data folder')