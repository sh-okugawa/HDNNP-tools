# coding: utf-8
import shutil

"""
This script is for creating folder of /Si-190808/1000K-LC7/mix/3500smpl
 with copying 3500 sample xyz
"""

## Modifying xyz data file name and mixing beta of TrainingConfig.py
def fileEdit1(fname, dataname):
    index1= 'c.TrainingConfig.data_file ='
    text1= "c.TrainingConfig.data_file = './data/"+dataname+"'\n"
    
    with open(fname, 'r') as infl:
        tmp_list =[]
        for row in infl:
            if row.find(index1) != -1:
                tmp_list.append(text1)
            else:
                tmp_list.append(row)

    with open(fname, 'w') as f2:
        for ii in range(len(tmp_list)):
            f2.write(tmp_list[ii])

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
    LC7folder="/home/okugawa/HDNNP/Si-190808/1000K-LC7/"
    datafolder="/home/okugawa/HDNNP/Si-190808/datas/1000K-LC7/"
    dirorgin = "/home/okugawa/HDNNP/Si-190808/base"
    grps=['mix']

    for grp in grps:
        for j in range(1,11):
            dataname= "1000K"+grp+"-3500-"+str(j)+".xyz"
            wkfolder=LC7folder+grp+"/3500smpl/"+str(j)
            datadestn = wkfolder+"/data"
            dataorgin= datafolder+grp+"/"+dataname
        
            shutil.copytree(dirorgin, wkfolder)
            shutil.copy2(dataorgin, datadestn)

            trncnffname = wkfolder+"/training_config.py"
            fileEdit1(trncnffname, dataname)
            fname1 = wkfolder+"/predict-phonopy/phonopyPrep.py"
            fname2 = wkfolder+"/predict-phono3py/phono3pyPrep.py"
            fileEdit2(fname1, wkfolder)
            fileEdit2(fname2, wkfolder)
            
        print(f'Create /Si-200917/1000K-LC7/{grp}/3500smpl data folder')