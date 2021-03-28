# coding: utf-8
import shutil

"""
This script is for creating folder of Si-amorphous with
amrSi103040-3000.xyz data and multiple Rc & SymmFunc
"""

## Modifying xyz data file name of TrainingConfig.py
def fileEdit1(fname, dataname, Rc):
    index1= 'c.TrainingConfig.data_file ='
    text1= "c.TrainingConfig.data_file = './data/"+dataname+"'\n"
    index2= '(6.5,'
    reptext= "("+Rc+","

    with open(fname, 'r') as infl:
        tmp_list =[]
        for row in infl:
            if row.find(index1) != -1:
                tmp_list.append(text1)
            elif row.find(index2) != -1:
                text2=row.replace(index2,reptext)
                tmp_list.append(text2)
            else:
                tmp_list.append(row)

    with open(fname, 'w') as f2:
        for ii in range(len(tmp_list)):
            f2.write(tmp_list[ii])

if __name__ == '__main__': 
    amr216folder="/home/okugawa/HDNNP/Si-amr/amr216/"
    symFfolder=amr216folder+"1500-103040smpl/SymF/"
    TCfolder=amr216folder+"TrainConfig/"
    base=amr216folder+"base"
    rcgrps= ["6.0","7.0","7.5"]
    dtgrps= ["org","SMZ"]
    dataname= "amrSi103040-1500.xyz"
    dataorgin= "/home/okugawa/HDNNP/Si-amr/datas/"+dataname
    
    #Multiple Rc parameters
    for rcgrp in rcgrps:
        for i in range(1, 11):
            wkfolder=symFfolder+"Rc/"+rcgrp+"/"+str(i)
            datadestn = wkfolder+"/data"
            trncnffname = wkfolder+"/training_config.py"
            shutil.copytree(base, wkfolder)
            shutil.copy2(dataorgin, datadestn)
            fileEdit1(trncnffname, dataname, rcgrp)
        print(f'Create /Si-amr/amr216/1500-103040smpl/SymF/Rc/{rcgrp} folder')
        
    #Multiple Symm_func 
    for dtgrp in dtgrps:
        TCfile=TCfolder+"training_config-"+dtgrp+".py"
        for i in range(1, 11):
            wkfolder=symFfolder+"SF/"+dtgrp+"/"+str(i)
            datadestn = wkfolder+"/data"
            trncnffname = wkfolder+"/training_config.py"
            shutil.copytree(base, wkfolder)
            shutil.copy2(dataorgin, datadestn)
            shutil.copy2(TCfile, trncnffname)
            fileEdit1(trncnffname, dataname, "6.5")
        print(f'Create /Si-amr/amr216/1500-103040smpl/SymF/SF/{dtgrp} folder')