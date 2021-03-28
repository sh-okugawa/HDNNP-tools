#!/bin/csh
#$ -cwd
#$ -V -S /bin/bash
#$ -N PlotSymF
#$ -o stdout
#$ -e stderr
#$ -q all.q
#$ -pe smp 24

PIPENV_PIPFILE=$HOME/HDNNP/Pipfile
pipenv run python plotSymF-TP.py