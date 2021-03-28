#!/bin/csh
#$ -cwd
#$ -V -S /bin/bash
#$ -N PlotSymFdiff
#$ -o pltSFdiffout
#$ -e pltSFdiffderr
#$ -q all.q
#$ -pe smp 4

PIPENV_PIPFILE=$HOME/HDNNP/Pipfile
pipenv run python chkSymFdiff.py