#!/usr/bin/env python
# coding: utf-8

"""
This script is for merging multiple xyz files to one
"""
  
if __name__ == '__main__': 
    datafolder="/home/okugawa/HDNNP/Si-amr/datas/"
    amrgrps=["amrSi10","amrSi30","amrSi40"]

    xyz1500=datafolder+"amrSi103040-1500.xyz"
    xyz3000=datafolder+"amrSi103040-3000.xyz"
    input500, input1000= [],[]

    for grp in amrgrps:
        in500=datafolder+grp+"-500.xyz"
        in1000=datafolder+grp+"-1000.xyz"
        input500.append(in500)
        input1000.append(in1000)

    with open(xyz1500, 'w') as out1500:
        for fname in input500:
            with open(fname) as infile:
                for line in infile:
                    out1500.write(line)

    with open(xyz3000, 'w') as out3000:
        for fname in input1000:
            with open(fname) as infile:
                for line in infile:
                    out3000.write(line)