# coding: utf-8
import random
import sys, os
import shutil

"""
This script is for picking up mixed 700 samples randomly from
5000 xyz data of 1000K LC=0.99,1.0,1.01 got by MD
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
    outfolder=mdfolder+"datas/"
    orgflds=['1000K0.99','1000K1.0','1000K1.01']
    fldname='1000Kmix'
    datanum=[233,234,233]
    mixdata=[]

    #generate mixed xyz data by picking up samples from original MD data
    for orgnum,orgfld in enumerate(orgflds):
        orgxyzfile=outfolder+"MDdata/"+orgfld+"all.xyz"
        
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
                smpfld=outfolder+fldname+"/"+str(i)
                if not os.path.isdir(smpfld):
                    os.makedirs(smpfld)
                xyzfile=smpfld+"/"+fldname+"-700.xyz"
                samples=random.sample(orglist,datanum[orgnum])
                
                with open(xyzfile, mode='a') as xyz:
                    for sample in samples:
                        for line in sample:
                            xyz.write(line)
                
                print(f'1000Kmix-{str(i)}: {len(samples)} samples are \
                      picked up from {datalen} data of {orgfld}')
                            
    #create data folders
    dirorgin = mdfolder+"base"
    datafolder = mdfolder+"datas/"

    print(f'Create {fldname} data folder')
    for i in range(1,11):
        wkfolder=mdfolder+fldname+"/"+str(i)
        dataname=fldname+"-700.xyz"
        dataorgin=datafolder+fldname+"/"+str(i)+"/"+dataname
        datadestn = wkfolder+"/data"
        
        shutil.copytree(dirorgin, wkfolder)
        shutil.copy2(dataorgin, datadestn)
        trncnffname = wkfolder+"/training_config.py"
        
        fileEdit1(trncnffname, dataname)
        fname1 = wkfolder+"/predict-phonopy/phonopyPrep.py"
        fname2 = wkfolder+"/predict-phono3py/phono3pyPrep.py"
        fileEdit2(fname1, wkfolder)
        fileEdit2(fname2, wkfolder)