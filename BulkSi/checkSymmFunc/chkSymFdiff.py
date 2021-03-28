# -*- coding: utf-8 -*-
import sys
import numpy as np
import matplotlib.pyplot as plt

"""
This script is calculating the Euclid distance (L2 norm) 
between Symmetry Function of Train and Predict 
"""

def plotGdiff(root, outfolder, grps, md):
    boxdic={"facecolor" : "lightcyan", "edgecolor" : "navy"}
    for grp in grps:
        plotfile1=outfolder+grp+"-SymFdiff.png"
        if grp=='mix':
            datadir=root+grp+"/1/1"
        else:
            datadir=root+grp+"/1"
        symfft=datadir+"/data/CrystalSi64/symmetry_function.npz"
        symt= np.load(symfft)
        symdtt= symt['sym_func']
        symffp=datadir+"/predict-phono3py-2/output-phono3py/symmetry_function-pred.npz"
        symp= np.load(symffp)
        symdtp= symp['sym_func']

        #Plot histgram of diff and report its ave and number of same-G        
        diffSF=diffSymF(symdtt, symdtp)
        txt1="Total data#= "+str(len(diffSF[0]))+"\n"
        txt2="   (Train smpl:  "+str(len(symdtt))+")\n"
        txt3="   (TC-predict:  "+str(len(symdtp))+")\n"
        txt4="   (Atoms/smpl:  "+str(diffSF[1])+")\n"
        txt5="Ave of L2= "+str(f'{diffSF[3]:.05f}')+"\n"
        txt6="Min of L2= "+str(f'{diffSF[4]:.05f}')
        L2txt=txt1+txt2+txt3+txt4+"\n"+txt5+txt6

        fig = plt.figure()
        ax = fig.add_subplot(111)
        xlbl="L2 norm of "+str(diffSF[2])+" Symm_Func diff"
        ttl="["+md+"/"+grp+"] Histgram of "+xlbl
        plt.title(ttl)
        ax.set_xlabel(xlbl)
        ax.hist(diffSF[0],bins=50)
        ax.text(0.98,0.97,L2txt,size=8,ha='right',va='top',
         transform=ax.transAxes,bbox=boxdic,multialignment='left')
        plt.savefig(plotfile1)
        plt.close()
        
def diffSymF(Tsymf,Psymf):
    #Calculate diff of Symmetry Function (compared corresponding atom#) and L2 norm
    totL2, totave= [],[]
    totmin=10000
    for Tsym in Tsymf:
        Psave=[]
        for Psym in Psymf:
            L2Ts= []
            if len(Tsym)!=len(Psym):
                print(f"Atom num Error: Train={len(Tsym)} & Predict={len(Psym)}")
                sys.exit()
            for i,Ts in enumerate(Tsym):
                Ps= Psym[i]
                if len(Ts)!=len(Ps):
                    print(f"SymF Len Error: Train={len(Ts)} & Predict={len(Ps)}")
                    sys.exit()
                symfdiff=Ts-Ps
                #L2 norm = sqrt of sum of squares
                L2nrm=np.linalg.norm(symfdiff,ord=2)
                L2Ts.append(L2nrm)
            aves=sum(L2Ts)/len(L2Ts)
            mins=min(L2Ts)
            if mins < totmin:
                totmin=mins
            Psave.append(aves)
            totL2.extend(L2Ts)
        totave.append(sum(Psave)/len(Psave))
    aves=sum(totave)/len(totave)
    return([totL2,len(Tsym),len(Ts),aves,totmin])
    
if __name__ == '__main__': 
    #calculate the diff of AIMD LC7 Symm_Func of Train & Predict
    LC7root="/home/okugawa/HDNNP/Si-190808-md/1000K-LC7n/"
    outfolder="/home/okugawa/HDNNP/Si-190808-md/result-LC7n/SymFdiff/"
    grps=['0.95','0.97','0.99','1.0','1.01','1.03','1.05','mix']
    plotGdiff(LC7root,outfolder,grps,"AIMD-LC7")    