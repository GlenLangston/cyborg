# python script to write an Arm command into shared memory
# HISTORY
# 11APR09AUG29 GIL try a wider bandwidth (not power of two)
# 09AUG12 GIL Wuppi version of status
# 09MAY18 P?D fix library path and to allow calling of g.update_azza()
# 09MAY18 GIL initial version
import corr
import time

fpga=corr.katcp_wrapper.FpgaClient('169.254.128.41',7147)
time.sleep(.05)
fpga.write_int('ARM',0)
time.sleep(.05)
fpga.write_int('ARM',1)
exit()

