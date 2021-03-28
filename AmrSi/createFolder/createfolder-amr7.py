# coding: utf-8
import shutil

"""
This script is for creating folder of Si-amorphous with
amrsi40-1000.xyz and amrSi103040-10001500/3000.xyz data
"""

## Modifying xyz data file name of TrainingConfig.py
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

if __name__ == '__main__': 
    amr216folder="/home/okugawa/HDNNP/Si-amr/amr216/"
    base1=amr216folder+"base"
    mqgrps= ["103040","103040","103040"]
    dtgrps= ["1000","1500","3000"]
    
    for nn,mqgrp in enumerate(mqgrps):
        dataname="amrSi"+mqgrp+"-"+dtgrps[nn]+".xyz"
        dataorgin= "/home/okugawa/HDNNP/Si-amr/datas/"+dataname
        for i in range(1, 11):
            wkfolder=amr216folder+dtgrps[nn]+"-"+mqgrp+"smpl/"+str(i)
            datadestn = wkfolder+"/data"
            shutil.copytree(base1, wkfolder)
            shutil.copy2(dataorgin, datadestn)
            trncnffname = wkfolder+"/training_config.py"
            fileEdit1(trncnffname, dataname)
            
        print(f'Create /Si-amr/amr216/{dtgrps[nn]}-{mqgrp}smpl folder')