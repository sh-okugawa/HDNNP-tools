#!/bin/csh
#$ -cwd
#$ -V -S /bin/bash
#$ -N PlotTC&L2
#$ -o TCL2out
#$ -e TCL2err
#$ -q all.q
#$ -pe smp 4

PIPENV_PIPFILE=$HOME/HDNNP/Pipfile
pipenv run python plotcorrL2TC.py