# -*- coding: utf-8 -*-
import shutil

"""
This script is creating folder for checking impact of PCA decomposition
by new procedure of PCA (only by train data)
Folders of Train and Phonopy, Phono3py are copied from base folder
and modified TrainingConfig and Phono(3)pyPrep of each.
"""

## Modifying xyz data file name of TrainingConfig.py
def fileEdit1(trncnffname, dataname, grp):
    index1= 'c.TrainingConfig.data_file ='
    text1= "c.TrainingConfig.data_file = './data/"+dataname+"'\n"
    index2= "c.DatasetConfig.preprocesses = ["
    text2= "#c.DatasetConfig.preprocesses = [\n"
    index3= "    ('pca', ("
    text3= "    ('pca', ("+grp+",), {}),\n"
    text4= "#    ('pca', (,), {}),\n"
    index5= "    ]"
    text5= "#    ]\n"

    with open(trncnffname, 'r') as infl:
        tmp_list =[]
        if grp=="noPCA":
            prerow=0
            for row in infl:
                if row.find(index1) != -1:
                    tmp_list.append(text1)
                elif row.find(index2) != -1:
                    tmp_list.append(text2)
                    prerow+=1
                elif row.find(index3) != -1:
                    tmp_list.append(text4)
                    prerow+=10
                elif row.find(index5) != -1:
                    if prerow==11:
                        tmp_list.append(text5)
                        prerow=0
                    else:
                        tmp_list.append(row)
                else:
                    tmp_list.append(row)
        else:
            for row in infl:
                if row.find(index1) != -1:
                    tmp_list.append(text1)
                elif row.find(index3) != -1:
                    tmp_list.append(text3)
                else:
                    tmp_list.append(row)

    with open(trncnffname, 'w') as f2:
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
    dirorgin=root+"base"
    dataname="all20.xyz"
    dataorgin=root+"d20n50/1/data/all20.xyz"
    grps=["10","15","20","30","noPCA"]
                            
    #create data folders
    for grp in grps:
        if grp!="noPCA":
            grpname="p"+grp
        else:
            grpname=grp
        for j in range(1, 11):
            dirdest = root+"d20n50-PCA/"+grpname+"/"+str(j)
            datadestn = dirdest+"/data"
            shutil.copytree(dirorgin, dirdest)
            shutil.copy2(dataorgin, datadestn)
    
            trncnffname = dirdest+"/training_config.py"
            fileEdit1(trncnffname, dataname, grp)
            fname1 = dirdest+"/predict-phonopy/phonopyPrep.py"
            fname2 = dirdest+"/predict-phono3py/phono3pyPrep.py"
            fileEdit2(fname1, dirdest)
            fileEdit2(fname2, dirdest)