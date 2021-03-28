# -*- coding: utf-8 -*-
import os
import shutil

"""
This script is for copying 3 files of /predict-phono3py folder and
modifying "bte_command" by removing '--sym-fc' parameter
"""
            
if __name__ == '__main__': 
    root=os.getcwd()

    bsxs=["d20n50"]
    copiedfile=['POSCAR-unitcell','phono3pyPrep.py','phono3pyRun.py']

    index1= 'bte_command=['
    text1= "bte_command=['phono3py',strpa, strdim, strmesh , '-c', poscar_seed, '--fc3', '--fc2', '--br' ]\n"
    index2= 'fc_command=['
    text2=  "fc_command=['phono3py', strdim, '-c', poscar_seed ]\n"
        
    for bsx in bsxs:
        for j in range(1, 11):
            shutil.rmtree(root+"/"+bsx+"/"+str(j)+"/predict-phono3py2")
            os.makedirs(root+"/"+bsx+"/"+str(j)+"/predict-phono3py2")
            dirorg = root+"/"+bsx+"/"+str(j)+"/predict-phono3py/"
            dirdest = root+"/"+bsx+"/"+str(j)+"/predict-phono3py2"

            for cpf in copiedfile:
                shutil.copy2(dirorg+cpf, dirdest)

            fname=dirdest+"/"+cpf
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

            print(f'Copied {bsx}/{j}')