# python script to read the 43m status line and set shared memory values
# HISTORY
# 09AUG12 GIL Wuppi version of status
# 09MAY18 P?D fix library path and to allow calling of g.update_azza()
# 09MAY18 GIL initial version
from guppi_utils import *
from astro_utils import current_MJD
from optparse import OptionParser
import os
import time

response = "                                                              "
cmd = "/users/glangsto/linux/realTime/gb43mRtClient -g deimos.gb.nrao.edu"
sin, sout = os.popen4(cmd)
response = sout.readline()
source, raStr, decStr, raDeg, decDeg, fmhzStr, bwmhzStr = response.split()
print source
exit

