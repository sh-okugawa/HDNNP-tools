# coding: utf-8
import shutil
import os

"""
This script is for creating folder of Si-amorphous with
sample20.xyz data (300 samples)
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

if __name__ == '__main__': 
    amr300folder="/home/okugawa/HDNNP/Si-amr/amr216/300smpl/"

    #create data folders
    dirorgin = "/home/okugawa/HDNNP/Si-amr/amr216/421smpl/2/"
    dataname = "sample20.xyz"
    dataorgin= "/home/okugawa/HDNNP/Si-amr/datas/"+dataname
    cnfgorgin = dirorgin+"training_config.py"
    runorgin = dirorgin+"run.csh"
    
    for i in range(1,11):
        wkfolder=amr300folder+str(i)
        datadestn = wkfolder+"/data"
        
        os.makedirs(datadestn)
        shutil.copy2(dataorgin, datadestn)
        shutil.copy2(cnfgorgin, wkfolder)
        shutil.copy2(runorgin, wkfolder)
        trncnffname = wkfolder+"/training_config.py"
        fileEdit1(trncnffname, dataname)
            
        print(f'Create /Si-amr/amr216/300smpl/{str(i)} data folder')