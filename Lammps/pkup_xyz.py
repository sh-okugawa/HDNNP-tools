#!/usr/bin/env python
# coding: utf-8
import random
import pathlib
import sys

"""
This script is for making 8 kind of xyz data of 700 samples
with specific combination of LC(Lattice constant) and Temperature
 1. all(7) of LC with 300K [100x7]
 2. all(7) of LC with 900K [100x7]
 3. all(7) of LC with 1500K [100x7]
 4. all(7) of LC with 600K(20),900K(60),1200K(20) [(20+60+20)x7]
 5. LC=0.97(100)&0.98(40) with all(5) temperature [(100+40)x5]
 6. LC=0.99(20)&1.00(100)&1.01(20) with all(5) temperature [(20+100+20)x5]
 7. LC=1.02(40)&1.03(100) with all(5) temperature [(40+100)x5]
 8. LC=0.99/T=600K(70),LC=0.99/T=900K(80),LC=0.99/T=1200K(70),
    LC=1.00/T=600K(80),LC=1.00/T=900K(100),LC=1.00/T=1200K(80),
    LC=1.01/T=600K(70),LC=1.01/T=900K(80),LC=1.01/T=1200K(70)  [700]

Put this script under LAMMPS folder which has "LC_TEMP" subfolder
like as "scale0.97_300K". Other subfolder should not be existed.
"""
  
if __name__ == '__main__': 
    outfolder="/home/okugawa/LAMMPS/out/"
    logfile=outfolder+"log.txt"
    
    samples=[["bs1", [["300K",100]]],
             ["bs2", [["900K",100]]],
             ["bs3", [["1500K",100]]],
             ["bs4", [["600K",20],["900K",60],["1200K",20]]],
             ["bs5", [["0.97",100],["0.98",40]]],
             ["bs6", [["0.99",20],["1.00",100],["1.01",20]]],
             ["bs7", [["1.02",40],["1.03",100]]],
             ["bs8", [["0.99","600K",70],["0.99","900K",80],["0.99","1200K",70],
                      ["1.00","600K",80],["1.00","900K",100],["1.00","1200K",80],
                      ["1.01","600K",70],["1.01","900K",80],["1.01","1200K",70]]]]

    for smp in samples:
        xyzfile=outfolder+smp[0]+"-700.xyz"
        LCTs=smp[1]
        
        with open(xyzfile, mode='w') as xyz, open(logfile, mode='a') as log:
            targets=[]
            present=pathlib.Path('./')
            dirs=([p for p in present.iterdir() if p.is_dir()])

            for dir in dirs:
                dirstr=str(dir)
                for LCT in LCTs:
                    if len(LCT)==3:
                        if all(xx in dirstr for xx in (LCT[0], LCT[1])):
                            subdirs=([s for s in dir.iterdir() if s.is_dir()])
                            targets+=random.sample(subdirs,LCT[2])
                    elif len(LCT)==2:
                        if LCT[0] in dirstr:
                            subdirs=([s for s in dir.iterdir() if s.is_dir()])
                            targets+=random.sample(subdirs,LCT[1])
                    else:
                        print(f'Format of picking up sample is not valid')
                        sys.exit()
                            
            print(f'{smp[0]} total collected samples: {len(targets)}')
            
            for target in targets:
                with open(str(target)+'/data.xyz', mode='r') as f:
                    lines=f.readlines()
                    for l in lines:
                        xyz.write(l)
                        
                log.write(str(target)+'\n')
            