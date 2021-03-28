# coding: utf-8
import shutil

"""
This script is for creating folder of Si-amorphous with
amrsi10-500/1000/1471.xyz data for 200 node & 2 layer
"""

## Modifying xyz data file name of TrainingConfig.py
def fileEdit1(fname, mixbeta, dataname):
    index1= 'c.TrainingConfig.data_file ='
    text1= "c.TrainingConfig.data_file = './data/"+dataname+"'\n"
    index2= '    {"mixing_beta":0.99}'
    text2= '    {"mixing_beta":'+mixbeta+'}\n'

    with open(fname, 'r') as infl:
        tmp_list =[]
        for row in infl:
            if row.find(index1) != -1:
                tmp_list.append(text1)
            elif row.find(index2) != -1:
                tmp_list.append(text2)
            else:
                tmp_list.append(row)

    with open(fname, 'w') as f2:
        for ii in range(len(tmp_list)):
            f2.write(tmp_list[ii])

if __name__ == '__main__': 
    amr216folder="/home/okugawa/HDNNP/Si-amr/amr216/"
    base1=amr216folder+"base"
    base2=amr216folder+"base2"
    grps= ["500","1000"]
    smplID= "30"
    
    for grp in grps:
        dataname="amrSi"+smplID+"-"+grp+".xyz"
        dataorgin= "/home/okugawa/HDNNP/Si-amr/datas/"+dataname
        for i in range(1, 11):
            wkfolder=amr216folder+grp+"-"+smplID+"smpl/"+str(i)
            datadestn = wkfolder+"/data"
            shutil.copytree(base1, wkfolder)
            shutil.copy2(dataorgin, datadestn)
            trncnffname = wkfolder+"/training_config.py"
            fileEdit1(trncnffname, "0.99", dataname)
            
        print(f'Create /Si-amr/amr216/{grp}-{smplID}smpl folder')