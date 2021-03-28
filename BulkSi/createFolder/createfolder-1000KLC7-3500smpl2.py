# coding: utf-8
import shutil
import random
import sys

"""
This script is for creating 3500 mix xyz data (randomly pick up 500samples from 
 each 7-LC xyz data) and creating folder of /Si-200917/1000K-LC7/mix/3500smpl
 with copying created 3500 sample xyz
"""

## Modifying xyz data file name and mixing beta of TrainingConfig.py
def fileEdit1(fname, dataname, j):
    index1= 'c.TrainingConfig.data_file ='
    text1= "c.TrainingConfig.data_file = './data/"+dataname+"'\n"
    index2= '{"mixing_beta":0.99}'
    text2= '    {"mixing_beta":0.5}\n'
    
    with open(fname, 'r') as infl:
        tmp_list =[]
        for row in infl:
            if row.find(index1) != -1:
                tmp_list.append(text1)
            elif row.find(index2) != -1:
                if j<11:
                    tmp_list.append(text2)
                else:
                    tmp_list.append(row)
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
    LC7folder=lmpfolder+"1000K-LC7/"
    orgdatafolder=lmpfolder+"datas/1000K-LC7/"
    orgflds=['0.95','0.97','0.99','1.00','1.01','1.03','1.05']
    fldname='mix'
    datanum1=3500
    datanum2=500

    #generate mixed xyz data by picking up samples from original MD data
    mixdtfld=orgdatafolder+"mix"

    for orgfld in orgflds :
        orgxyzfile=orgdatafolder+"LC7data/"+orgfld+".xyz"
        
        with open(orgxyzfile, mode='r') as org:
            lines=org.readlines()
            datalen, mod = divmod(len(lines), 66)
            if mod != 0:
                print(f'Error: Data length of {orgfld} is not 66x')
                sys.exit()
            orglist=[]
            orgdata=[]
            
            for i,line in enumerate(lines):
                orgdata.append(line)
                if (i % 66)==65:
                    orglist.append(orgdata)
                    orgdata=[]
            
            for i in range(1,11):
                mixxyzfile=mixdtfld+"/1000Kmix-"+str(datanum1)+"-"+str(i)+".xyz"
                mixsamples=random.sample(orglist,datanum2) 
                
                with open(mixxyzfile, mode='a') as mixxyz:
                    for sample in mixsamples:
                        for line in sample:
                            newline=line.replace("config_type=","tag=")
                            #replace "config_type=" included in old xyz file to "tag="
                            mixxyz.write(newline)
                            
        msg2=str(len(mixsamples))+' samples of 1000Kmix are '
        msg3='picked up from '+str(datalen)+' data of '+orgfld+'.xyz'
        print(msg2+msg3)
                
    #create data folders
    LC7folder="/home/okugawa/HDNNP/Si-200917/1000K-LC7/"
    datafolder="/home/okugawa/HDNNP/Si-190808/datas/1000K-LC7/"
    dirorgin = "/home/okugawa/HDNNP/Si-190808/base"
    grps=['mix']

    for grp in grps:
        for j in range(1,21):
            if j>10:
                dataname= "1000K"+grp+"-3500-"+str(j-10)+".xyz"
            else:
                dataname= "1000K"+grp+"-3500-"+str(j)+".xyz"
            wkfolder=LC7folder+grp+"/3500smpl/"+str(j)
            datadestn = wkfolder+"/data"
            dataorgin= datafolder+grp+"/"+dataname
        
            shutil.copytree(dirorgin, wkfolder)
            shutil.copy2(dataorgin, datadestn)

            trncnffname = wkfolder+"/training_config.py"
            fileEdit1(trncnffname, dataname, j)
            fname1 = wkfolder+"/predict-phonopy/phonopyPrep.py"
            fname2 = wkfolder+"/predict-phono3py/phono3pyPrep.py"
            fileEdit2(fname1, wkfolder)
            fileEdit2(fname2, wkfolder)
            
        print(f'Create /Si-200917/1000K-LC7/{grp}/3500smpl data folder')