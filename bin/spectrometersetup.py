 
# For Configuring the registers in the 20-m Spectrometer 
import corr, struct,time
import socket,pylab
import numpy as np

fpga=corr.katcp_wrapper.FpgaClient('169.254.128.41',7147)
time.sleep(5)
fpga.progdev('')
time.sleep(5)
fpga.progdev('.bof')
time.sleep(5)


# List of Registers in the Skynet Switching Signal Spectrometer Design
# This spectrometer outputs switching signals to the receiver room from the GPIO on the ROACH
 
 #'snappol1_ctrl' - This register is to take snapshot of raw FFT output from POL1 
 #'snappol0_ctrl' - This register is to take snapshot of raw FFT output from POL0
 #'snap_adc1_ctrl' - This register is to take snapshot of the raw data from ADC1 - Can be used to plot the histogram
 #'snap_adc0_ctrl' - This register is to take snapshot of the raw data from ADC0 - Can be used to plot the histogram
 #'SSG_LENGTH'
 #'SSG_GRANULARITY'
 #'SSG_BRAM'
 #'SCALE_V'
 #'SCALE_U'
 #'SCALE_Q'
 #'SCALE_I'
 #'OFFSET_V'
 #'OFFSET_U'
 #'OFFSET_Q'
 #'OFFSET_I'
 #'FFT_SHIFT'
 #'DEST_PORT'
 #'DEST_IP'
 #'ARM'
 #'ACC_LEN'
 
# Reading the raw ADC data samples from two polarizations -

# To plot the raw samples from the ADC follow the below mentioned note
# If the number is greater than 128, subtract the byte with 256 else make no changes to that number if you are using the National ADC

fpga.write_int('snap_adc0_ctrl',1)
time.sleep(0.5)
adc0=fpga.snapshot_get('snap_adc0')
adc0_data=adc0['data']

fpga.write_int('snap_adc1_ctrl',1)
time.sleep(0.5)
adc1=fpga.snapshot_get('snap_adc1')
adc1_data=adc1['data']


# Reading the raw FFT data from two polarizations - You will be able to take the data only after ARMING THE PFB
# Each channel is Ufix_32_0

fpga.write_int('snappol0_ctrl',1)
time.sleep(0.5)
pol0=fpga.snapshot_get('snappol0')
pol0_data=pol0['data']


fpga.write_int('snappol1_ctrl',1)
time.sleep(0.5)
pol1=fpga.snapshot_get('snappol1')
pol1_data=pol1['data']



# Writing values in to the Switching Signal Generator 
fpga.write('SSG_BRAM',struct.pack('>L',524295),offset=4*0)
time.sleep(0.5)
fpga.write('SSG_BRAM',struct.pack('>L',7864326),offset=4*1)
time.sleep(0.5)
fpga.write('SSG_BRAM',struct.pack('>L',32773),offset=4*2)
time.sleep(0.5)
fpga.write('SSG_BRAM',struct.pack('>L',8355844),offset=4*3)
time.sleep(0.5)
fpga.write('SSG_BRAM',struct.pack('>L',524291),offset=4*4)
time.sleep(0.5)
fpga.write('SSG_BRAM',struct.pack('>L',7864322),offset=4*5)
time.sleep(0.5)
fpga.write('SSG_BRAM',struct.pack('>L',32769),offset=4*6)
time.sleep(0.5)
fpga.write('SSG_BRAM',struct.pack('>L',8355840),offset=4*7)
time.sleep(0.5)
fpga.write_int('SSG_LENGTH',1048576)
time.sleep(0.5)
fpga.write_int('SSG_GRANULARITY',256)
time.sleep(0.5)

DEST_IP=192*(2**24)+168*(2**16)+3*(2**8)+15
time.sleep(0.5)
DEST_PORT=52000
time.sleep(0.5)
SOURCE_IP=192*(2**24)+168*(2**16)+3*(2**8)+13
time.sleep(0.5)
FABRIC_PORT=63000
time.sleep(0.5)
MAC_BASE=(2<<32)+(2<<40)
time.sleep(0.5)

fpga.write_int('DEST_PORT',DEST_PORT)
time.sleep(0.5)
fpga.write_int('DEST_IP',DEST_IP)
time.sleep(0.5)

fpga.write_int('ACC_LEN',511)
time.sleep(0.5)
fpga.write_int('FFT_SHIFT',0xDFDFDFDF)
time.sleep(0.5)


fpga.write_int('SCALE_I',150000)
time.sleep(0.5)
fpga.write_int('SCALE_Q',150000)
time.sleep(0.5)
fpga.write_int('SCALE_U',150000)
time.sleep(0.5)
fpga.write_int('SCALE_V',150000)
time.sleep(0.5)

fpga.write_int('OFFSET_I',0)
time.sleep(0.5)
fpga.write_int('OFFSET_Q',0)
time.sleep(0.5)
fpga.write_int('OFFSET_U',0)
time.sleep(0.5)
fpga.write_int('OFFSET_V',0)
time.sleep(0.5)

fpga.tap_start('tap1','ten_GbE',MAC_BASE,SOURCE_IP,FABRIC_PORT)
time.sleep(0.5)
fpga.write_int('ARM',0)
time.sleep(1)
fpga.write_int('ARM',1)
time.sleep(0.25)
fpga.write_int('ARM',0)




# For Reading the data from 10 GbE
print 'Starting data capture ...'
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('',52000))
file=open('skynet_1024chan_jray.bin','wb')
for i in range(100000):
	x=s.recv(10000)
	file.write(x)

file.close()
toc=time.clock()
tictoc=toc-tic
print tictoc
import time

import socket,pylab
import numpy as np
tic=time.clock()


# For Plotting the switching Signals
a=np.fromfile('sample_ssg_skynet_512acclen.bin',dtype=uint16).byteswap()
b=reshape(a,[100000,4112]
c=b[:,4103]
f=np.zeros([100000,3])
for i in range(0,100000):
	e=binary_repr(c[i],3)
	for j in range(0,3):
	f[i,j]=e[j]

figure()
x=np.arange(0,4000,1)
subplot(3,1,1)
step(x,f[:,0]
ylime([-1,1.5])

subplot(3,1,2)
step(x,f[:,0]
ylime([-1,1.5])


subplot(3,1,3)
step(x,f[:,0]
ylime([-1,1.5])


