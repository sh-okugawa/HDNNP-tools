# coding: utf-8
import random
import sys

"""
This script is for picking up 1000 samples randomly from 1500 xyz data of
1000K LC3(0.99,1.00,1.01) got by LAMMPS-MD and merging to 3000 sample data
"""
  
if __name__ == '__main__': 
    lmpfolder="/home/okugawa/HDNNP/Si-190808/"
    LC7folder=lmpfolder+"1000K-LC7/"
    orgdatafolder=lmpfolder+"datas/1000K-LC7/"
    orgflds=['0.99','1.00','1.01']
    datanum2=1000

    #generate mixed xyz data by picking up samples from original MD data
    mixdtfld=orgdatafolder+"mix3"

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
                mixxyzfile=mixdtfld+"/1000Kmix-3000-"+str(i)+".xyz"
                mixsamples=random.sample(orglist,datanum2) 
                
                with open(mixxyzfile, mode='a') as mixxyz:
                    for sample in mixsamples:
                        for line in sample:
                            newline=line.replace("config_type=","tag=")
                            #replace "config_type=" included in old xyz file to "tag="
                            mixxyz.write(newline)
                            
                msg1=str(len(mixsamples))+' samples of 1000Kmix are '
                msg2='picked up from '+str(datalen)+' data of '+orgfld+'.xyz'
                print(msg1+msg2)