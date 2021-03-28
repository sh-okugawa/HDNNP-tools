# coding: utf-8
import shutil

"""
This script is for creating folder of Si-amorphous with
sample20.xyz data for 40/100/200 node & 2/3/4/5 layer
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
                text2= "   ("+node+", 'tanh'),\n"
                for i in range(layer):
                    tmp_list.append(text2)
            else:
                tmp_list.append(row)

    with open(fname, 'w') as f2:
        for ii in range(len(tmp_list)):
            f2.write(tmp_list[ii])

if __name__ == '__main__': 
    amr216folder="/home/okugawa/HDNNP/Si-amr/amr216/"
    base=amr216folder+"base"
    dataname = "sample20.xyz"
    nodes= ["40","100","200"]
    dataorgin= "/home/okugawa/HDNNP/Si-amr/datas/"+dataname
    
    for node in nodes:
        for layer in range(2, 6):
            for i in range(1, 6):
                wkfolder=amr216folder+"300smpl/"+node+"-"+str(layer)+"/"+str(i)
                datadestn = wkfolder+"/data"
                shutil.copytree(base, wkfolder)
                shutil.copy2(dataorgin, datadestn)
                trncnffname = wkfolder+"/training_config.py"
                fileEdit1(trncnffname, node, layer, dataname)
            
        print(f'Create /Si-amr/amr216/300smpl/{node}-{str(layer)} data folder')