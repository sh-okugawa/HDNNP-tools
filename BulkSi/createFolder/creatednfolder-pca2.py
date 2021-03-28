# -*- coding: utf-8 -*-
import shutil

"""
This script is creating folder for reducing dimension of PCA as 10,15,20 
Folders of Train and Phonopy, Phono3py are copied from seed folder
and modified TrainingConfig and Phono(3)pyPrep of each.
Seed folder must be existed in [current dir]/d20n50-xxx/1 in advance
"""

## Modifying output directory name of phonopyPrep.py and phono3pyPrep.py
def fileEdit(fname, root, grp, j):
    index= 'nnpout='
    text= "nnpout='"+root+"d20n50-"+grp+"/"+str(j)+"/output'\n"

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
    grps=["p30","noPCA"]

    for grp in grps:
        dirorg = root+"d20n50-"+grp+"/1"
        for j in range(1, 11):
            dirdest = root+"d20n50-"+grp+"/"+str(j)
            if j != 1:
                shutil.copytree(dirorg, dirdest)  ## copy seed dir
            fname1 = dirdest+"/predict-phonopy/phonopyPrep.py"
            fname2 = dirdest+"/predict-phono3py/phono3pyPrep.py"
            fileEdit(fname1, root, grp, j)
            fileEdit(fname2, root, grp, j)