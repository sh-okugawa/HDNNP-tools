# -*- coding: utf-8 -*-

"""
This script is for outputting x/y/z axis data of all structure
as txt file from xyz file
"""

if __name__ == '__main__': 
    datafolder="/home/okugawa/HDNNP/Si-amr/datas/"
    xyzfile=datafolder+"sample20.xyz"
    outputfolder=datafolder+"xyz/300smpl/"
    tag="Si"
    datanum=216
    
    with open(xyzfile,'r') as fxyz:
        nn=0
        alldatas=[]
        data1 =[]
        
        for line in fxyz:
            data=line.split()
            if data[0]==tag:
                wdt=data[1]+" "+data[2]+" "+data[3]
                data1.append(wdt)
                nn+=1
                if nn==datanum:
                    alldatas.append(data1)
                    nn=0
                    data1=[]
    
    LENall=len(alldatas)
    
    for i,smpl in enumerate(alldatas):
        out1file=outputfolder+"xyz-{:03d}.txt".format(i)
        with open(out1file,'w') as out1:
            for dt in smpl:
                out1.write(dt+"\n")

    print(f'{LENall} of all x/y/z data are output to txt file')  