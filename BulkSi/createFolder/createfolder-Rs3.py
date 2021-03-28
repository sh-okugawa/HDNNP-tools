# coding: utf-8
import shutil

"""
This script is for creating folder of G2:Rs=0 (training_config.py)
of LAMMPS-MD 1000Kmix7 with copying mixed 700 sample xyz 
from /datas/1000K-LC7/mix
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
    lmpfolder="/home/okugawa/HDNNP/Si-190808/"
    LC7mixfolder=lmpfolder+"1000K-LC7/Rs/mix/"
    orgmixdatafolder=lmpfolder+"datas/1000K-LC7/mix/"

    #create data folders
    dirorgin = lmpfolder+"base"
    cnfgorgin = lmpfolder+"base-cnfg/training_config3.py"
    for i in range(1,11):
        dataname="1000Kmix-700-"+str(i)+".xyz"
        dataorgin=orgmixdatafolder+dataname
        wkfolder=LC7mixfolder+"3/"+str(i)
        datadestn = wkfolder+"/data"
        cnfgdstn = wkfolder+"/training_config.py"
    
        shutil.copytree(dirorgin, wkfolder)
        shutil.copy2(dataorgin, datadestn)
        shutil.copy2(cnfgorgin, cnfgdstn)
        trncnffname = wkfolder+"/training_config.py"
        
        fileEdit1(trncnffname, dataname)
        fname1 = wkfolder+"/predict-phonopy/phonopyPrep.py"
        fname2 = wkfolder+"/predict-phono3py/phono3pyPrep.py"
        fileEdit2(fname1, wkfolder)
        fileEdit2(fname2, wkfolder)
            
        print(f'Create /1000K-LC7/Rs/mix/3/{str(i)} data folder')