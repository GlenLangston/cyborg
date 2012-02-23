# python script to read the 43m status line and set shared memory values
# HISTORY
# 09OCT28 GIL set the DM for an individual pulsar
# 09AUG29 GIL try a wider bandwidth (not power of two)
# 09AUG12 GIL Wuppi version of status
# 09MAY18 P?D fix library path and to allow calling of g.update_azza()
# 09MAY18 GIL initial version
from guppi_utils import *
from astro_utils import current_MJD
from optparse import OptionParser
import os
import time
import sys

g = guppi_status()
source = "PSR1937+21"
#mjd = astro.current_MJD()
#mjd = "55159"
mjd = sys.argv[1]
source = g["SRC_NAME"]
scannum = sys.argv[2]
base = "cyborg_" + mjd + "_" + source + "_" + scannum
g.update("BASENAME", base)
g.update("BACKEND", "CYBORG")

g.write()
exit

