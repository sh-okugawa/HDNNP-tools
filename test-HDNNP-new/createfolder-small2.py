# coding: utf-8
import shutil

"""
This script is for creating folder of /Si-200917/1000K-LC7/ for updated HDNNP
 with copying sample xyz from /HDNNP-org/Si-190808/datas/1000K-LC7/
"""

## Modifying xyz data file name and mixing beta of TrainingConfig.py
def fileEdit1(fname, dataname):
    index1= 'c.TrainingConfig.data_file ='
    text1= "c.TrainingConfig.data_file = './data/"+dataname+"'\n"
    index2= '    {"mixing_beta":0.5}'
    text2= '    {"mixing_beta":0.99}\n'
    
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

## Modifying Pipfile name of run.csh
def fileEdit3(fname, pipfile):
    index1= 'PIPENV_PIPFILE='
    text1= "PIPENV_PIPFILE="+pipfile+"\n"
    
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
    smallfolder="/home/okugawa/test-HDNNP-new/HDNNP/Si-200917/small/"
    datafolder="/home/okugawa/HDNNP/Si-190808/datas/small/"
    dirorgin = "/home/okugawa/HDNNP/Si-190808/base"
    dataname= "small.xyz"
    dataorgin= datafolder+dataname
    tcorgin= datafolder+"training_config.py"
    pipfile= "/home/okugawa/test-HDNNP-new/HDNNP/Pipfile"

    #create data folders
    for j in range(11,21):
        wkfolder=smallfolder+str(j)
        datadestn = wkfolder+"/data"
    
        shutil.copytree(dirorgin, wkfolder)
        shutil.copy2(dataorgin, datadestn)
        shutil.copy2(tcorgin, wkfolder)

        trncnffname = wkfolder+"/training_config.py"
        fileEdit1(trncnffname, dataname)
        fname1 = wkfolder+"/predict-phonopy/phonopyPrep.py"
        fname2 = wkfolder+"/predict-phono3py/phono3pyPrep.py"
        fileEdit2(fname1, wkfolder)
        fileEdit2(fname2, wkfolder)
        runfname = wkfolder+"/run.csh"
        fileEdit3(runfname, pipfile)
        
    print(f'Create /test-HDNNP-new/HDNNP/Si-200917/small data folder')