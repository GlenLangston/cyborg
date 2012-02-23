# python script to write an Arm command into the Roach board register
# HISTORY
# 12JAN25 GIL clean up comments
# 11APR09 GIL try a wider bandwidth (not power of two)
# 09MAY18 GIL initial version
import corr
import time

#setup the 100 Mbps link to the roach board
fpga=corr.katcp_wrapper.FpgaClient('169.254.128.41',7147)
time.sleep(.05)
fpga.write_int('ARM',0)
time.sleep(.05)
fpga.write_int('ARM',1)
exit()

