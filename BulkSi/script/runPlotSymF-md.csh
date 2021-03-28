#!/bin/csh
#$ -cwd
#$ -V -S /bin/bash
#$ -N Plot-SymFunc
#$ -o stdout
#$ -e stderr
#$ -q all.q
#$ -pe smp 1

PIPENV_PIPFILE=$HOME/HDNNP/Pipfile
pipenv run python plotSymF-G-md.py