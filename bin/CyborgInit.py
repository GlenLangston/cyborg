# python script to read the 43m status line and set shared memory values
# HISTORY
# 12FEB22 GIL change the defaults for slower data acquistion
# 12FEB16 GIL change the defaults for slower data acquistion
# 11APR14 GIL/SB new roach design
# 10MAY03 GIL/SSB revise packet format back to 1SFA
# 10APR14 GIL packet format for Ruppi
# 09AUG29 GIL try a wider bandwidth (not power of two)
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
ra = float(raDeg)
dec = float(decDeg)
bwMHz = 500.0
sideFlip = 1
freqMHz = float(fmhzStr)
freqMHz = 1.5*bwMHz
freqMHz = 10000.0
nChan   = 1024
if (sideFlip==1):
    chanMHz = -bwMHz/nChan
else:
    chanMHz = bwMHz/nChan
g = guppi_status()
g.update("TELESCOP", "GB43m")
g.update("BACKEND", "CYBORG")
g.update("SRC_NAME", source)
g.update("RA_STR", raStr)
g.update("DEC_STR", decStr)
g.update("RA", ra)
g.update("DEC", dec)
if (sideFlip==1):
    g.update("OBSBW", -bwMHz)
else:
    g.update("OBSBW", bwMHz)
g.update("FRONTEND", "Rx0.15-1.7")
g.update("DATAHOST", "roach2_10")
#g.update("DATAHOST", "roach3_10")
g.update("OBSERVER", "Skynet/Glen")
g.update("OBSFREQ", freqMHz)
g.update("OBSNCHAN", nChan)
#g.update("STRTFREQ", 288.0)
#g.update("STOPFREQ", 688.0)
g.update("STRTFREQ", freqMHz-(bwMHz/2.))
g.update("STOPFREQ", freqMHz+(bwMHz/2.))
g.update("DATAPORT", 52000)
g.update("PKTFMT", "1SFA")
#g.update("PKTFMT", "PARKES")
g.update("CHAN_BW", chanMHz)
#add the accumulation length for WuppiStatus startup
g.update("ACC_LEN",  16)
# The design double clocks the sampler so 500MHz clock 1 Giga samples/sec
# for 500 MHz clock, 512  spectra = 1024*2*512/(2*500E6)  s = 0.00105 seconds
# for 500 MHz clock, 1024 spectra = 1024*2*1024/(2*500E6) s = 0.0021 seconds
g.update("ACC_LEN",  1024)
g.update("POL_TYPE", "INTEN")
#
g.update("NBIN", 1024)
g.update("NBITS", 16)
g.update("NBITSADC", 8)
g.update("ONLY_I", 0)
#g.update("NBITS", 8)
#g.update("NBITSADC", 8)
#
g.update("NPOL",  4)
#g.update("BLOCSIZE", 2097152)
g.update("BLOCSIZE", 1048576)

# now update az and zenith angle and write values
g.update_azza()
g.write()
exit

