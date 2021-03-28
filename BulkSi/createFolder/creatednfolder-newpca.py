# -*- coding: utf-8 -*-
import shutil

"""
This script is creating folder for new procedure of PCA 
Folders of Train and Phonopy, Phono3py are copied from seed folder
and modified TrainingConfig and Phono(3)pyPrep of each.
Seed folder must be existed in [current dir]/d20n50-xxx/1 in advance
"""

## Modifying xyz data file name of TrainingConfig.py
def fileEdit1(fname, dataname):
    index= 'c.TrainingConfig.data_file ='
    text= "c.TrainingConfig.data_file = './data/"+dataname+"'\n"

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
def fileEdit2(fname, dirdest):
    index= 'nnpout='
    text= "nnpout='"+dirdest+"/output'\n"

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
    root="/home/okugawa/HDNNP/Si-190808/"
    dirorgin="/home/okugawa/HDNNP/Si-190808-md/base"
    dataname="all20.xyz"
    dataorgin=root+"d20n50/1/data/"+dataname
                            
    #create data folders
    for j in range(1, 11):
        dirdest = root+"d20n50-newPCA/"+str(j)
        datadestn = dirdest+"/data"
        shutil.copytree(dirorgin, dirdest)
        shutil.copy2(dataorgin, datadestn)

        trncnffname = dirdest+"/training_config.py"
        fileEdit1(trncnffname, dataname)
        fname1 = dirdest+"/predict-phonopy/phonopyPrep.py"
        fname2 = dirdest+"/predict-phono3py/phono3pyPrep.py"
        fileEdit2(fname1, dirdest)
        fileEdit2(fname2, dirdest)
