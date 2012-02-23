# python script to read the 43m status line and set shared memory values
# HISTORY
# 12FEB13 GIL Cyborg version of status
# 09AUG12 GIL Wuppi version of status
# 09MAY18 P?D fix library path and to allow calling of g.update_azza()
# 09MAY18 GIL initial version
from guppi_utils import *
from astro_utils import current_MJD
from optparse import OptionParser
import os
import time

while True:
    response = "                                                              "
    cmd = "/users/glangsto/linux/realTime/gb43mRtClient -g deimos.gb.nrao.edu"
    sin, sout = os.popen4(cmd)
    response = sout.readline()
    source, raStr, decStr, raDeg, decDeg, fmhzStr, bwmhzStr = response.split()
    ra = float(raDeg)
    dec = float(decDeg)
    freqMHz = float(fmhzStr)
    nChan   = 2048
    chanMHz = freqMHz/nChan
    bwMHz = freqMHz
    g = guppi_status()
    g.update("SRC_NAME", source)
    g.update("RA_STR", raStr)
    g.update("DEC_STR", decStr)
    g.update("RA", ra)
    g.update("DEC", dec)

# This script is running on cicada in
# /export/home/cicada2/scratch/glangsto
# the following line 
    g.update_azza()
    g.write()
# now wait a while
    time.sleep(0.50)
   
