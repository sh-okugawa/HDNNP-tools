#!/usr/bin/env python
# coding: utf-8
import random
import pathlib
import sys

"""
This script is for making 7 kind of xyz data of 2100 samples
with specific combination of LC(Lattice constant) and Temperature
 1. TL2-L7: all(7) of LC with 300K,600K [150x7x2]
 2. TML2-L7: all(7) of LC with 600K,900K [150x7x2]
 3. TMH2-L7: all(7) of LC with 900K,1200K [150x7x2]
 4. TH2-L7: all(7) of LC with 1200K,1500K [150x7x2]
 5. TL3-LM5: LC=0.98&0.99&1.00&1.01&1.02 with 300K,600K,900K [140x5x3]
 6. TM3-LM5: LC=0.98&0.99&1.00&1.01&1.02 with 600K,900K,1200K [140x5x3]
 7. TH3-LM5: LC=0.98&0.99&1.00&1.01&1.02 with 900K,1200K,1500K [140x5x3]

Put this script under LAMMPS folder which has "LC_TEMP" subfolder
like as "scale0.97_300K". Other subfolder should not be existed.
"""
  
if __name__ == '__main__': 
    outfolder="/home/okugawa/LAMMPS/out/"
    logfile=outfolder+"log3.txt"

    samples=[["TL2-L7", [["300K",150],["600K",150]]],
             ["TML2-L7", [["600K",150],["900K",150]]],
             ["TMH2-L7", [["900K",150],["1200K",150]]],
             ["TH2-L7", [["1200K",150],["1500K",150]]],
             ["TL3-LM5", [["0.98","300K",140],["0.98","600K",140],["0.98","900K",140],
                      ["0.99","300K",140],["0.99","600K",140],["0.99","900K",140],
                      ["1.00","300K",140],["1.00","600K",140],["1.00","900K",140],
                      ["1.01","300K",140],["1.01","600K",140],["1.01","900K",140],
                      ["1.02","300K",140],["1.02","600K",140],["1.02","900K",140]]],
             ["TM3-LM5", [["0.98","600K",140],["0.98","900K",140],["0.98","1200K",140],
                      ["0.99","600K",140],["0.99","900K",140],["0.99","1200K",140],
                      ["1.00","600K",140],["1.00","900K",140],["1.00","1200K",140],
                      ["1.01","600K",140],["1.01","900K",140],["1.01","1200K",140],
                      ["1.02","600K",140],["1.02","900K",140],["1.02","1200K",140]]],
             ["TH3-LM5", [["0.98","900K",140],["0.98","1200K",140],["0.98","1500K",140],
                      ["0.99","900K",140],["0.99","1200K",140],["0.99","1500K",140],
                      ["1.00","900K",140],["1.00","1200K",140],["1.00","1500K",140],
                      ["1.01","900K",140],["1.01","1200K",140],["1.01","1500K",140],
                      ["1.02","900K",140],["1.02","1200K",140],["1.02","1500K",140]]]]

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