#!/usr/bin/env python
# coding: utf-8
import random
import pathlib
import sys

"""
This script is for making 6 kind of xyz data of 2100&900 samples
with specific combination of LC(Lattice constant) and Temperature
 1. TL3-L7: all(7) of LC with 300K,600K,900K [100x7x3]
 2. TM3-L7: all(7) of LC with 600K,900K,1200K [100x7x3]
 3. TH3-L7: all(7) of LC with 900K,1200K,1500K [100x7x3]
 4. TL3-LM3: LC=0.99&1.00&1.01 with 300K,600K,900K [100x3x3]
 5. TM3-LM3: LC=0.99&1.00&1.01 with 600K,900K,1200K [100x3x3]
 6. TH3-LM3: LC=0.99&1.00&1.01 with 900K,1200K,1500K [100x3x3]
 7. TL3-L7-9: all(7) of LC with 300K,600K,900K [43x7x3]
 8. TM3-L7-9: all(7) of LC with 600K,900K,1200K [43x7x3]
 9. TH3-L7-9: all(7) of LC with 900K,1200K,1500K [43x7x3]

Put this script under LAMMPS folder which has "LC_TEMP" subfolder
like as "scale0.97_300K". Other subfolder should not be existed.
"""
  
if __name__ == '__main__': 
    outfolder="/home/okugawa/LAMMPS/out/"
    logfile=outfolder+"log2.txt"

    samples=[["TL3-L7", [["300K",100],["600K",100],["900K",100]]],
             ["TM3-L7", [["600K",100],["900K",100],["1200K",100]]],
             ["TH3-L7", [["900K",100],["1200K",100],["1500K",100]]],
             ["TL3-LM3", [["0.99","300K",100],["0.99","600K",100],["0.99","900K",100],
                      ["1.00","300K",100],["1.00","600K",100],["1.00","900K",100],
                      ["1.01","300K",100],["1.01","600K",100],["1.01","900K",100]]],
             ["TM3-LM3", [["0.99","600K",100],["0.99","900K",100],["0.99","1200K",100],
                      ["1.00","600K",100],["1.00","900K",100],["1.00","1200K",100],
                      ["1.01","600K",100],["1.01","900K",100],["1.01","1200K",100]]],
             ["TH3-LM3", [["0.99","900K",100],["0.99","1200K",100],["0.99","1500K",100],
                      ["1.00","900K",100],["1.00","1200K",100],["1.00","1500K",100],
                      ["1.01","900K",100],["1.01","1200K",100],["1.01","1500K",100]]],
             ["TL3-L79", [["300K",43],["600K",43],["900K",43]]],
             ["TM3-L79", [["600K",43],["900K",43],["1200K",43]]],
             ["TH3-L79", [["900K",43],["1200K",43],["1500K",43]]]]

    for smp in samples:
        xyzfile=outfolder+smp[0]+".xyz"
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
            