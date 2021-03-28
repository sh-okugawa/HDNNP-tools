# coding: utf-8
import shutil

"""
This script is for creating folder of Si-amorphous with
amrsi-315/786.xyz data for 200 node & 2 layer
"""

## Modifying xyz data file name of TrainingConfig.py
def fileEdit1(fname, node, layer, dataname):
    index1= 'c.TrainingConfig.data_file ='
    text1= "c.TrainingConfig.data_file = './data/"+dataname+"'\n"
    index2= "   (node, 'tanh'),"

    with open(fname, 'r') as infl:
        tmp_list =[]
        for row in infl:
            if row.find(index1) != -1:
                tmp_list.append(text1)
            elif row.find(index2) != -1:
                text2= "   ("+str(node)+", 'tanh'),\n"
                for i in range(layer):
                    tmp_list.append(text2)
            else:
                tmp_list.append(row)

    with open(fname, 'w') as f2:
        for ii in range(len(tmp_list)):
            f2.write(tmp_list[ii])

def fileEdit2(fname):
    index1= '#$ -pe smp 24'
    text1= "#$ -pe smp 8\n"
    index2= 'pipenv run mpirun -np 24 hdnnpy train'
    text2= "pipenv run mpirun -np 8 hdnnpy train"

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
    base=amr216folder+"base"
    
    for grp in range(3,5):
        dataname="amrsi"+str(grp)+"-105.xyz"
        dataorgin= "/home/okugawa/HDNNP/Si-amr/datas/"+dataname
        for i in range(1, 11):
            wkfolder=amr216folder+"105-"+str(grp)+"smpl/"+str(i)
            datadestn = wkfolder+"/data"
            shutil.copytree(base, wkfolder)
            shutil.copy2(dataorgin, datadestn)
            trncnffname = wkfolder+"/training_config.py"
            fileEdit1(trncnffname, 200, 2, dataname)
            runfname = wkfolder+"/run.csh"
            fileEdit2(runfname)
            
        print(f'Create /Si-amr/amr216/105-{grp}smpl folder')