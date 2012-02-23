# python script to write an Arm command into shared memory
# HISTORY
# 11APR09AUG29 GIL try a wider bandwidth (not power of two)
# 09AUG12 GIL Wuppi version of status
# 09MAY18 P?D fix library path and to allow calling of g.update_azza()
# 09MAY18 GIL initial version
import corr
import time
import sys
fpga=corr.katcp_wrapper.FpgaClient('169.254.128.41',7147)
time.sleep(.25)

nargs = len(sys.argv)

#for i in range(0,nargs):
#    print i, sys.argv[i]
    
if nargs < 2:
    acclen = 1023
else:
    acclen = int(sys.argv[nargs-1])

print 'ACC_LEN: ',acclen
fpga.write_int('ACC_LEN',acclen)
time.sleep(.25)
readAccLen = fpga.read_int('ACC_LEN')
print 'ACC_LEN Read:',readAccLen
exit()

