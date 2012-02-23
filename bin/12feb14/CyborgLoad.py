# python script to write an Arm command into shared memory
# HISTORY
# 11APR09AUG29 GIL try a wider bandwidth (not power of two)
# 09AUG12 GIL Wuppi version of status
# 09MAY18 P?D fix library path and to allow calling of g.update_azza()
# 09MAY18 GIL initial version
import corr
import time

fpga=corr.katcp_wrapper.FpgaClient('169.254.128.41',7147)

time.sleep(.25)
#fpga.listbof()
#time.sleep(.25)
fpga.progdev('')
time.sleep(.25)
#fpga.progdev('ruppi_1024ch_4tap_iquv_2011_Apr_19_1837.bof')
fpga.progdev('skynet_1024ch_4tap_2012_Jan_19_1413.bof')
time.sleep(.25)
#fpga.listdev()
#time.sleep(.25)

fpga.write_int('FFT_SHIFT',0xDFDFDFFF)
#fpga.write_int('fft_shift',0xDFDFDFFF)
fpga.write_int('OFFSET_I',0)
time.sleep(.25)
fpga.write_int('OFFSET_Q',0)
time.sleep(.25)
fpga.write_int('OFFSET_U',0)
time.sleep(.25)
fpga.write_int('OFFSET_V',0)
time.sleep(.25)

#fpga.write_int('SCALE_I',150000)
scaleI = 150000
scaleQ = 150000
fpga.write_int('SCALE_I',scaleI) 
time.sleep(.25)
fpga.write_int('SCALE_Q',scaleQ)
time.sleep(.25)
fpga.write_int('SCALE_U',scaleQ)
time.sleep(.25)
fpga.write_int('SCALE_V',scaleQ)
time.sleep(.25)

DEST_IP=192*(2**24)+168*(2**16)+3*(2**8)+15
DEST_PORT=52000
SOURCE_IP=192*(2**24)+168*(2**16)+3*(2**8)+13
FABRIC_PORT=63000
MAC_BASE=(2<<32)+(2<<40)

fpga.write_int('DEST_IP',DEST_IP)
time.sleep(.25)
fpga.write_int('DEST_PORT',DEST_PORT)
time.sleep(.25)
fpga.write_int('ACC_LEN',31)
time.sleep(.25)
fpga.tap_start('tap1','ten_GbE',MAC_BASE,SOURCE_IP,FABRIC_PORT)
time.sleep(.05)

fpga.write_int('ARM',0)
time.sleep(.05)
fpga.write_int('ARM',1)
time.sleep(.05)
fpga.write_int('ARM',0)
exit()

