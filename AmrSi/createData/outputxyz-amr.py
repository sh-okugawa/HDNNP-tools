# -*- coding: utf-8 -*-
import sys
import random

"""
This script is for outputting x/y/z axis data from xyz file
$ python outputxyz-amr.py [number of 1-structure axis data]   
"""

if __name__ == '__main__': 
    datafolder="/home/okugawa/HDNNP/Si-amr/datas/"
    xyzfile=datafolder+"sample225+10.xyz"
    outallfile=datafolder+"xyz/471smpl/xyzall.txt"
    tag="Si"
    datanum=216
    
    args = sys.argv
    filenum = int(args[1])

    with open(xyzfile,'r') as fxyz, open(outallfile, 'w') as fout:
        nn=0
        alldatas=[]
        data1 =[]
        
        for line in fxyz:
            data=line.split()
            if data[0]==tag:
                wdt=data[1]+" "+data[2]+" "+data[3]
                fout.write(wdt+"\n")
                data1.append(wdt)
                nn+=1
                if nn==datanum:
                    alldatas.append(data1)
                    nn=0
                    data1=[]
    
    LENall=len(alldatas)
    
    samples=random.sample(alldatas,filenum)
    for i,smpl in enumerate(samples):
        out1file=datafolder+"xyz/471smpl/xyz-"+str(i+1)+".txt"
        with open(out1file,'w') as out1:
            for dt in smpl:
                out1.write(dt+"\n")

    print(f'{LENall} of all x/y/z data and {filenum} of picked up x/y/z data are output')