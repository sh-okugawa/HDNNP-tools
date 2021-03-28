# -*- coding: utf-8 -*-
import os
import shutil

"""
This script is creating folder for bad sample 
Folders of Train and Phonopy, Phono3py are copied from seed folder
and modified TrainingConfig and Phono(3)pyPrep of each.
xyz data should be existed in [current dir]/datas folder and 
seed folder must be existed in [current dir]/bs1-dxxn50/1 in advance 
"""

## Modifying xyz data file name of TrainingConfig.py
def fileEdit1(fname, bsx):
    index= 'c.TrainingConfig.data_file ='
    text= "c.TrainingConfig.data_file = './data/"+bsx+"-700.xyz'\n"

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

## Modifying output directory name of phonopyPrep.py and phono3pyPrep.py
def fileEdit2(fname, root, bsx, j):
    index= 'nnpout='
    text= "nnpout='"+root+"/"+bsx+"-d20n50"+"/"+str(j)+"/output'\n"

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
    root=os.getcwd()

    bsxs=["bs1","bs2","bs3","bs4","bs5","bs6","bs7","bs8"]
        
    dirorgin = root+"/bs1-d20n50/1"
    datafolder = root+"/datas/"
        
    for bsx in reversed(bsxs):
        print(f'Create {bsx} data folder')
        dirdestn = root+"/"+bsx+"-d20n50/1"
        dataorgin = datafolder+bsx+"-700.xyz"
        datadestn = dirdestn+"/data"
        if bsx == bsxs[0]:
            shutil.copy2(dataorgin, datadestn)
        else:
            shutil.copytree(dirorgin, dirdestn)
            shutil.copy2(dataorgin, datadestn)

        bs=bsx
        for j in range(1, 11):
            dirorg = root+"/"+bsx+"-d20n50/1"
            dirdest = root+"/"+bsx+"-d20n50/"+str(j)
            if j != 1:
                shutil.copytree(dirorg, dirdest)  ## copy seed dir
            trncnffname = dirdest+"/training_config.py"
            fileEdit1(trncnffname, bs)
            fname1 = dirdest+"/predict-phonopy/phonopyPrep.py"
            fname2 = dirdest+"/predict-phono3py/phono3pyPrep.py"
            fileEdit2(fname1, root, bsx, j)
            fileEdit2(fname2, root, bsx, j)
             