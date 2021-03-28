# coding: utf-8
import shutil

"""
This script is for creating folder of /Si-200917/1000K-LC3/ for updated HDNNP
 with copying sample xyz from /HDNNP-org/Si-190808/datas/1000K-LC7/mix3
"""

## Modifying xyz data file name and mixing beta of TrainingConfig.py
def fileEdit1(fname, dataname):
    index1= 'c.TrainingConfig.data_file ='
    text1= "c.TrainingConfig.data_file = './data/"+dataname+"'\n"
    index2= "   (50, 'tanh'),"
    text2= "   (200, 'tanh'),\n"
    
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
def fileEdit2(fname, wkfolder, pipfile):
    index1= 'nnpout='
    text1= "nnpout='"+wkfolder+"/output'\n"
    index2= "pipfile='/home/okugawa/HDNNP/Pipfile'"
    text2= "pipfile='"+pipfile+"'\n"

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

## Modifying Pipfile directry of run.csh
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
    LC1folder="/home/okugawa/test-HDNNP-new/HDNNP/Si-200917/1000K-LC1/1500smpl/"
    LC3mixfolder="/home/okugawa/test-HDNNP-new/HDNNP/Si-200917/1000K-LC3/mix/3000smpl/"
    data1file="/home/okugawa/HDNNP/Si-190808/datas/1000K-LC7/LC7data/1.00.xyz"
    data3folder="/home/okugawa/HDNNP/Si-190808/datas/1000K-LC7/mix3/"
    dirorgin = "/home/okugawa/HDNNP/Si-190808/base"
    pipfile= "/home/okugawa/test-HDNNP-new/HDNNP/Pipfile"

    #create LC1 data folders
    for j in range(1,11):
        dataname= "1.00.xyz"
        wkfolder=LC1folder+str(j)
        datadestn = wkfolder+"/data"
    
        shutil.copytree(dirorgin, wkfolder)
        shutil.copy2(data1file, datadestn)

        trncnffname = wkfolder+"/training_config.py"
        fileEdit1(trncnffname, dataname)
        fname1 = wkfolder+"/predict-phonopy/phonopyPrep.py"
        fname2 = wkfolder+"/predict-phono3py/phono3pyPrep.py"
        fileEdit2(fname1, wkfolder, pipfile)
        fileEdit2(fname2, wkfolder, pipfile)
        runfname = wkfolder+"/run.csh"
        fileEdit3(runfname, pipfile)
          
    print(f'Create /1000K-LC1/1500smpl data folder')

    #create LC3 data folders
    for j in range(1,11):
        dataname= "1000Kmix-3000-"+str(j)+".xyz"
        wkfolder=LC3mixfolder+str(j)
        dataorgin= data3folder+dataname
        datadestn = wkfolder+"/data"
    
        shutil.copytree(dirorgin, wkfolder)
        shutil.copy2(dataorgin, datadestn)

        trncnffname = wkfolder+"/training_config.py"
        fileEdit1(trncnffname, dataname)
        fname1 = wkfolder+"/predict-phonopy/phonopyPrep.py"
        fname2 = wkfolder+"/predict-phono3py/phono3pyPrep.py"
        fileEdit2(fname1, wkfolder, pipfile)
        fileEdit2(fname2, wkfolder, pipfile)
        runfname = wkfolder+"/run.csh"
        fileEdit3(runfname, pipfile)
          
    print(f'Create /1000K-LC3/mix/3000smpl data folder')