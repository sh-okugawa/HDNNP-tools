# coding: utf-8
import shutil

"""
This script is for picking up mixed 700 samples randomly from
5000 xyz data of 1000K LC7(0.95,0.97,0.99,1.0,1.01,1,03,1.05) got by AIMD
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
    mdfolder="/home/okugawa/HDNNP/Si-190808-md/"
    LC7nfolder=mdfolder+"1000K-LC7n/"
    orgdatafolder=mdfolder+"datas/1000K-LC7/"
    orgflds=['0.95','0.97','0.99','1.00','1.01','1.03','1.05']

    #create each LC data folders
    dirorgin = mdfolder+"base"
    for orgfld in orgflds:
        smpfld=orgdatafolder+orgfld
        for i in range(1,11):
            wkfolder=LC7nfolder+orgfld+"/"+str(i)
            dataname="1000K"+orgfld+"-700"+"-"+str(i)+".xyz"
            dataorgin=smpfld+"/"+dataname
            datadestn = wkfolder+"/data"
            
            shutil.copytree(dirorgin, wkfolder)
            shutil.copy2(dataorgin, datadestn)
            trncnffname = wkfolder+"/training_config.py"
            
            fileEdit1(trncnffname, dataname)
            fname1 = wkfolder+"/predict-phonopy/phonopyPrep.py"
            fname2 = wkfolder+"/predict-phono3py/phono3pyPrep.py"
            fileEdit2(fname1, wkfolder)
            fileEdit2(fname2, wkfolder)
            
        print(f'Created /1000K-LC7n/{orgfld} data folder')
        
    #create mix data folders
    for i in range(1,11):
        dataname="1000Kmix7-700-"+str(i)+".xyz"
        dataorgin=orgdatafolder+"mix/"+dataname
        for j in range(1,11):
            wkfolder=LC7nfolder+"mix/"+str(i)+"/"+str(j)
            datadestn = wkfolder+"/data"
        
            shutil.copytree(dirorgin, wkfolder)
            shutil.copy2(dataorgin, datadestn)
            trncnffname = wkfolder+"/training_config.py"
            
            fileEdit1(trncnffname, dataname)
            fname1 = wkfolder+"/predict-phonopy/phonopyPrep.py"
            fname2 = wkfolder+"/predict-phono3py/phono3pyPrep.py"
            fileEdit2(fname1, wkfolder)
            fileEdit2(fname2, wkfolder)
            
        print(f'Create /1000K-LC7n/mix/{str(i)} data folder')