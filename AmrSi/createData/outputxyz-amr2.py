# -*- coding: utf-8 -*-

"""
This script is for outputting x/y/z axis data of all structure
as txt file from xyz file
"""

if __name__ == '__main__': 
    datafolder="/home/okugawa/HDNNP/Si-amr/datas/"
    xyzfile=datafolder+"sample225+10.xyz"
    outputfolder=datafolder+"xyz/471smpl/"
    tag="Si"
    datanum=216
    
    with open(xyzfile,'r') as fxyz:
        nn=0
        alldatas=[]
        data1 =[]
        xyzdt = fxyz.readlines()
        
        for line in xyzdt:
            data=line.split()
            if data[0]==tag:
                wdt=str(data[1])+" "+str(data[2])+" "+str(data[3])
                data1.append(wdt)
                nn+=1
                if nn==datanum:
                    alldatas.append(data1)
                    nn=0
                    data1=[]
    
    LENall=len(alldatas)
    print(f'alldatas[0][0]= {alldatas[0][0]}')
    print(f'alldatas[1][0]= {alldatas[1][0]}')
    print(f'alldatas[2][0]= {alldatas[2][0]}')
    print(f'alldatas[3][0]= {alldatas[3][0]}')
    LENall=len(alldatas)
    
    for i,smpl in enumerate(alldatas):
        out1file=outputfolder+"xyz-{:03d}.txt".format(i)
        with open(out1file,'w') as out1:
            for dt in smpl:
                out1.write(dt+"\n")

    print(f'{LENall} of all x/y/z data are output to txt file')  