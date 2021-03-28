# coding: utf-8
import random
import sys, os
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
    LC7folder=mdfolder+"1000K-LC7/"
    orgdatafolder=mdfolder+"datas/1000K-LC7/"
    orgflds=['0.95','0.97','0.99','1.0','1.01','1.03','1.05']
    datanum=700

    #generate mixed xyz data by picking up samples from original MD data
    for orgfld in orgflds :
        orgxyzfile=orgdatafolder+"LC7data/1000K"+orgfld+"all.xyz"
        
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
            
            smpfld=orgdatafolder+orgfld
            os.makedirs(smpfld)
            for i in range(1,11):
                xyzfile=smpfld+"/1000K"+orgfld+"-"+str(datanum)+"-"+str(i)+".xyz"
                samples=random.sample(orglist,datanum)
                
                with open(xyzfile, mode='w') as xyz:
                    for sample in samples:
                        for line in sample:
                            newline=line.replace("config_type=","tag=")
                            #replace "config_type=" included in old xyz file to "tag="
                            xyz.write(newline)

                msg1='1000K'+orgfld+'-'+str(i)+': '+str(len(samples))+' samples are '
                msg=msg1+'picked up from'+str(datalen)+' data of 1000K'+orgfld+'all.xyz'
                print(msg)
                
    #create data folders
    dirorgin = mdfolder+"base"
    for orgfld in orgflds:
        smpfld=orgdatafolder+orgfld
        for i in range(1,11):
            wkfolder=LC7folder+orgfld+"/"+str(i)
            dataname="1000K"+orgfld+"-"+str(datanum)+"-"+str(i)+".xyz"
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
            
        print(f'Created /1000K-LC7/{orgfld} data folder')