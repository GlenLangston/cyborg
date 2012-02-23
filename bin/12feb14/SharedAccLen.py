# python script to read the 43m status line and set shared memory values
# HISTORY
# 11APR14 GIL/SB new roach design
# 10MAY03 GIL/SSB revise packet format back to 1SFA
# 10APR14 GIL packet format for Ruppi
# 09AUG29 GIL try a wider bandwidth (not power of two)
# 09AUG12 GIL Wuppi version of status
# 09MAY18 P?D fix library path and to allow calling of g.update_azza()
# 09MAY18 GIL initial version
from guppi_utils import *
import sys
import time

nargs = len(sys.argv)
if nargs < 2:
    acclen = 16
else
    acclen = int(sys.argv[nargs-1])

g.update("ACC_LEN",  acclen)
g.write()
exit

