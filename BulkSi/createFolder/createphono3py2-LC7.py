# -*- coding: utf-8 -*-
import os
import shutil

"""
This script is for copying 3 files of /predict-phono3py folder and
modifying "bte_command"&"fc_command" by removing '--sym-fc' parameter
"""

def fileEdit(datadir):
    copiedfile=['POSCAR-unitcell','phono3pyPrep.py','phono3pyRun.py']
    index1= 'bte_command=['
    text1= "bte_command=['phono3py',strpa, strdim, strmesh , '-c', poscar_seed, '--fc3', '--fc2', '--br' ]\n"
    index2= 'fc_command=['
    text2=  "fc_command=['phono3py', strdim, '-c', poscar_seed ]\n"
    
    os.makedirs(datadir+"/predict-phono3py2")
    dirorg = datadir+"/predict-phono3py/"
    dirdest = datadir+"/predict-phono3py2"

    for cpf in copiedfile:
        shutil.copy2(dirorg+cpf, dirdest)

    fname=dirdest+"/phono3pyRun.py"
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
    root="/home/okugawa/HDNNP/Si-190808/1000K-LC7/"
    grps=['0.95','0.97','0.99','1.00','1.01','1.03','1.05','mix']
        
    for grp in grps:
        for i in range(1, 11):
            if grp=='mix':
                for j in range(1, 11):
                    datadir=root+grp+"/"+str(i)+"/"+str(j)
                    fileEdit(datadir)
                    
            else:
                datadir=root+grp+"/"+str(i)
                fileEdit(datadir)

        print(f'Copied phono3py of /1000K-LC7/{grp}')             