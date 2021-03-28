# -*- coding: utf-8 -*-
import Gnuplot

"""
This script is for plotting band data of phonopy by gnuplot
"""

g=Gnuplot.Gnuplot()
g(' set terminal pdf ')
g(' cd "/home/okugawa/HDNNP/Si-190808-md/1000K/1/predict-phonopy" ')
g(' set output "test.pdf" ')
g(' set xrange[0.0:1.074] ')
g(' set yrange[0.0:25.0] ')
g(' set xtics (" {/Symbol G} "  0.00000000," M "  0.17950810," K "  0.28314720,\
               " {/Symbol G} "  0.49042540," A "  0.58584590," L "  0.76535400,\
               " H"   0.86899310, "A" 1.074) ')
g(' set arrow from  0.179508100,  0.0 to  0.17950810,  25.0 nohead ')
g(' set arrow from  0.28314720,  0.0 to  0.28314720,  25.0 nohead ')
g(' set arrow from  0.49042540,  0.0 to  0.49042540,  25.0 nohead ')
g(' set arrow from  0.58584590,  0.0 to  0.58584590,  25.0 nohead ')
g(' set arrow from  0.76535400,  0.0 to  0.76535400,  25.0 nohead ')
g(' set arrow from  0.86899310,  0.0 to  0.86899310,  25.0 nohead ')
g(' set key outside below ')
g(' plot "band_data.gp" w l lt -1 lc rgb "red" lw 3 ti "HDNNP" ')
g(' set terminal wxt ')
g(' exit ')
