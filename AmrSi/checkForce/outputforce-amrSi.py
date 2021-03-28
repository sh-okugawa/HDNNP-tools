# -*- coding: utf-8 -*-
"""
This script is for outputting x/y/z axis data from xyz file
$ python outputforce-amr.py [file name of xyz under /Si-amr/datas/]   
"""
import sys

if __name__ == '__main__': 
    datafolder="/home/okugawa/HDNNP/Si-amr/datas/"
    tag="Si"
    datanum=216
    
    args = sys.argv
    xyzfile=datafolder+args[1]+".xyz"
    forcefile=datafolder+"force/"+args[1]+"f.txt"
    
    with open(xyzfile,'r') as fxyz, open(forcefile, 'w') as fout:
        for line in fxyz:
            data=line.split()
            if data[0]==tag:
                wdt=data[4]+" "+data[5]+" "+data[6]+"\n"
                fout.write(wdt)
                
    print(f'Force data file is created from /Si-amr/datas/{args[1]}.xyz')