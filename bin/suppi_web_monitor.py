#python code to monitor the Guppi/Wuppi buffer and creat a plot for
#Web monitoring of the data quality
#HISTORY
#12JAN18 GIL re-arrange data
#12JAN06 GIL Try to sort out the spectra/bits and chans 
#12JAN05 GIL work with new data 16bits 1024 chans, 4 stokes
#10MAR15 GIL prevent crash by checking vector size
#09DEC14 GIL do weighted average of 3 channels near peak
#09SEP25 GIL to reduce display flashing
#09SEP24 GIL try to fix web and realtime displays
#09SEP15 GIL Wuppi version, add lissting of max spectrum
#09JAN01 P?D initial working version
import sys, gtk, gobject, time
import matplotlib
matplotlib.use('GTKAgg')
from guppi_utils import guppi_status, guppi_databuf
from datetime import datetime
import shm_wrapper as shm
import os
import numpy as n
import pylab as p

nspec_sum = 128
iPol  = 0
plotCount = 0
polns = 'IQUV'
delay = 2.0
view_mean = True
view_dB = False
lastHour = -1
lastMinute = -1
npoln = 4
g = guppi_status()
g.read()
nChan = g["OBSNCHAN"]
npoln = g["NPOL"]
BW = g["OBSBW"]
fctr = g["OBSFREQ"]
blocksize = g["BLOCSIZE"]
bins = n.arange(nChan)
freqs = (bins/float(nChan))*BW + (fctr-0.5*BW)
ymin = 0.0
ymax = 2000.0
nspec_sum = blocksize/(2*nChan*npoln)
print 'N Spec: ', nspec_sum,blocksize,nChan,npoln

def dB(x, mindb=-80.0):
    return n.where(x>0, 10.0*n.log10(x/255.0), mindb)

def usage():
    print """
  SUPPI Real-Time Web Monitor
  ---------------------------
  This program provides a web-based real-time monitor for SUPPI data.
  There are several options to adjust plotting.  Position the mouse
  in the plotting window and press one of the following keys:
    '1-4':     Change the poln number to plot (1='I', 2='Q', etc)
    'i', 'o':  Zoom in/out of the X-axis
    '-', '+':  Zoom in/out of the Y-axis (no shift needed)
    'u', 'd':  Shift plot up/down in the window
    '<', '>':  Shift plot left/right in the window (no shift needed)
    'x', 'c':  Change X-axis units to/from frequency from/to channels
    'b':       Change Y-axis units to/from dB from/to linear scale
    'a':       Attempt to auto-scale the plot
    'm':       Set y axis to min and max of data
    's':       Toggle between the mean and standard deviation
    'q':       Quit the plotter
  You can also use the icons at the bottom of the window to scale, 
  shift, zoom, print etc.
    """

def key_press(event):
    global iPol, view_mean, view_dB, ymin, ymax, nspec_sum
    if event.key in 'io':    # Zoom in/out (x-direction)
        axes = main_line.get_axes()
        xlim = axes.get_xlim()
        midx = 0.5*(xlim[1]+xlim[0])
        dx = 0.5*(xlim[1]-xlim[0])
        if event.key=='i':  # Zoom in  by a factor of 2
            axes.set_xlim(midx-0.5*dx, midx+0.5*dx)
        else:               # Zoom out by a factor of 2
            axes.set_xlim(midx-2.0*dx, midx+2.0*dx)
    elif event.key in '=-': # Zoom in/out (y-direction)
        axes = main_line.get_axes()
        ylim = axes.get_ylim()
        midy = 0.5*(ylim[1]+ylim[0])
        dy = 0.5*(ylim[1]-ylim[0])
        if event.key=='=':  # Zoom in  by a factor of 2
            axes.set_ylim(midy-0.5*dy, midy+0.5*dy)
        else:               # Zoom out by a factor of 2
            axes.set_ylim(midy-2.0*dy, midy+2.0*dy)
    elif event.key in 'ud':  # Shift up/down by 20% of the y-height
        axes = main_line.get_axes()
        ylim = axes.get_ylim()
        dy = ylim[1]-ylim[0]
        if event.key=='d':   # Shift down
            axes.set_ylim(ylim+0.2*dy)
        else:                # Shift up
            axes.set_ylim(ylim-0.2*dy)
    elif event.key in 'm':   # set yminmax
        axes = main_line.get_axes()
        ylim = axes.get_ylim()
        print 'ylim: ', ylim
        ymin = main_spec[1:nChan-2].min(0)
        ymax = main_spec[1:nChan-2].max(0)
        print 'ymin: ', ymin
        print 'ymax: ', ymax
        axes.set_ylim([ymin,ymax])
    elif event.key in ',.':    # Shift right/left by 20% of the x-width
        axes = main_line.get_axes()
        xlim = axes.get_xlim()
        dx = xlim[1]-xlim[0]
        if event.key=='.':     # Shift right
            axes.set_xlim(xlim+0.2*dx)
        else:                  # Shift left
            axes.set_xlim(xlim-0.2*dx)
    elif event.key in 'xc':  # Freq to bins and vise-versa
        if ax.get_xlabel().startswith('Chan'):
            ax.set_xlabel('Frequency (MHz)')
            main_line.set_xdata(freqs)
            min_line.set_xdata(freqs)
            max_line.set_xdata(freqs)
            axes = main_line.get_axes()
            axes.set_xlim(freqs[0], freqs[-1])
        else:
            ax.set_xlabel('Channel Number')
            main_line.set_xdata(bins)
            min_line.set_xdata(bins)
            max_line.set_xdata(bins)
            axes = main_line.get_axes()
            axes.set_xlim(bins[0], bins[-1])
    #elif event.key=='l':  # Log axes
    #    axes = main_line.get_axes()
    #    axes.set_yscale('log')
    #    axes.autoscale_view()
    elif event.key=='a':  # Auto-scale
        axes = main_line.get_axes()
        axes.autoscale_view()
    elif event.key=='b': # dB scale
        view_dB = not view_dB
        axes = main_line.get_axes()
        ylim = axes.get_ylim()
        if view_dB:
            print "Changing power units to dB"
            axes.set_ylim(-50.0, 0.0)
            ax.set_ylabel('Un-calibrated Power (dB)')
        else:
            print "Changing power units to a linear scale"
            axes.set_ylim(-255.0, 255)
            ax.set_ylabel('Un-calibrated Power')
    elif event.key in '1234': # Switch polarization
        iPol = int(event.key)-1
        ax.set_title("Poln is '%s'"%polns[iPol])
    elif event.key=='s':  # Stats
        view_mean = not view_mean
        if view_mean: print "Main plot is average spectra"
        else: print "Main plot is spectra standard deviation"
    elif event.key=='q':  # Quit
        sys.exit()
    fig.canvas.draw()

def update_lines(*args):
    global lastMinute, lastHour, freqs, bins, nspec_sum
    g.read()
    try:
        curblock = g["CURBLOCK"]
    except KeyError:
        curblock = 1
    bdata = d.data(curblock)
    adata = n.fromstring( bdata, n.int16)
    data =  adata.byteswap()
    if bdata.ndim == 1:
        redata = n.reshape( data, (-1,nChan,1)) 
        if view_mean:
            main_spec = redata[:,:,0].mean(0)
        else:
            main_spec = redata[:,:,0].std(0)
        print 'bdata.ndim==1: ',main_spec.shape
        min_spec = redata[:nspec_sum,:nChan,0].min(0)
        max_spec = redata[:nspec_sum,:nChan,0].max(0)
    if bdata.ndim == 3:
        # turn bytes into short ints
#        adata = n.reshape( n.fromstring( data, n.int16), (nChan,1,-1))
#        print "data    X, Y, Z:", data.shape[0], data.shape[1], data.shape[2]
#        print "redata  X, Y, Z:", redata.shape[0], redata.shape[1], redata.shape[2]
# The following example shows how an array of 4 polarizations, 10 channels and
# six different, consecutive spectra are organized in a python array
# The input data are arranged as I0,Q0,U0,V0,I1,Q1,U1,V1,I2...
#>>> big = n.arange(4*10*6)
#>>> big = n.reshape(big,(6,10,4))
#>>> print big[0,:,3]               <-This gets first spectrum, last pol
#[ 3  7 11 15 19 23 27 31 35 39]   
#>>> print big[1,:,3]               <-This gets second spectrum, last pol
#[43 47 51 55 59 63 67 71 75 79]

# This section of the code is executed every cycle:
        nspec_sum = 256

        redata = n.reshape( data, (-1, nChan, npoln)) 
#        print 'n Spec:',nspec_sum
        n4 = 1
        n34 = nspec_sum -1
#        print 'R:',n.shape(redata),n4,n34
        nspec_sum = nspec_sum-1
#        min_spec = redata[:nspec_sum,:,iPol].min(0)
#        max_spec = redata[:nspec_sum,:,iPol].max(0)
        min_spec = redata[n4:n34,:,iPol].min(0)
        max_spec = redata[n4:n34,:,iPol].max(0)
        if view_mean:
#            main_spec = redata[:nspec_sum,:,iPol].mean(0)
            main_spec = redata[n4:n34,:,iPol].mean(0)
        else:
#            main_spec = redata[:nspec_sum,:,iPol].std(0)
            main_spec = redata[n4:n34,:,iPol].std(0)
#        if redata.shape[0] > nspec_sum:
#            if redata.shape[2] > npoln:
#                min_spec = redata[:nspec_sum,:,0].min(0)
#                max_spec = redata[:nspec_sum,:,0].max(0)
#                if view_mean:
#                    main_spec = redata[:nspec_sum,:,0].mean(0)
#                else:
#                    main_spec = redata[:nspec_sum,:,0].std(0)
    nX = main_spec.shape[0]
    nF = freqs.shape[0]
    if nF != nX:
        print 'nF != nX: ', nF, nX
        bins = n.arange(nX)
        freqs = (bins/float(nX))*BW + (fctr-0.5*BW)
        main_line.set_xdata(freqs)
        max_line.set_xdata(freqs)
        min_line.set_xdata(freqs)
    main_spec[0] = 0
#    print 'Shape main: ',n.shape(main_spec)
#    print 'Shape freq: ',n.shape(freqs)
#    print 'Shape min: ',n.shape(min_spec)
#    print 'Shape max: ',n.shape(max_spec)
    main_spec[nChan-1] = 0
    ymin = main_spec.min(0)
    ymax = main_spec.max(0)
    if view_dB:
        main_line.set_ydata(dB(main_spec))
        max_line.set_ydata(dB(max_spec))
        min_line.set_ydata(dB(min_spec))
    else:
        main_line.set_ydata(main_spec)
        max_line.set_ydata(max_spec)
        min_line.set_ydata(min_spec)
    idx = abs(main_spec).argmax()
    if idx < 1:
        idx = 1
    if idx > nChan-2:
        idx = nChan - 2
    sumMain = main_spec[idx-1] + main_spec[idx] + main_spec[idx+1]
    freqMaxA = main_spec[idx-1]*freqs[idx-1]/sumMain
    freqMaxB = main_spec[idx]*freqs[idx]/sumMain
    freqMaxC = main_spec[idx+1]*freqs[idx+1]/sumMain
    freqMax  = freqMaxA + freqMaxB + freqMaxC
#    print "Block %2d, poln '%s': Max chan=%d freq=%.3fMHz value=%.3f %.3f" %\
#      (curblock, polns[poln], idx-1, freqs[idx-1], main_spec[idx-1], freqMax)
#    print "Block %2d, poln '%s': Max chan=%d freq=%.3fMHz value=%.3f %.3f" %\
#          (curblock, polns[poln], idx, freqs[idx], main_spec[idx], freqMax)
#    print "Block %2d, poln '%s': Max chan=%d freq=%.3fMHz value=%.3f %.3f" %\
#       (curblock, polns[poln], idx+1, freqs[idx+1], main_spec[idx+1], freqMax)
    raStr = g["RA_STR"]
    decStr = g["DEC_STR"]
    source = g["SRC_NAME"]
    now = datetime.today()
    nowStr =now.strftime('%y/%m/%d %H:%M:%S')
    ax.set_title("%s: %s  %s,%s;  %s"%\
                 (polns[iPol], source, raStr, decStr, nowStr))
    if ax.get_xlabel().startswith('Chan'):
        ax.set_xlabel('Channel (Max %.3fMHz)'%freqMax)
    else:
        ax.set_xlabel('Frequency (MHz,  Max %.3fMHz)'%freqMax)
    fig.canvas.restore_region(background)
    
    ax.draw_artist(main_line)
    ax.draw_artist(max_line)
    ax.draw_artist(min_line)
    fig.canvas.blit(ax.bbox)
# try to get non-web display to update
    fig.canvas.draw()
#    time.sleep(delay)
    p.savefig('suppiBandpass.png',dpi=80)
    # keep plots evey hour to monitor spectrum
    hour = round(now.hour)
    # check monitoring with minutes (or 10s of minutes)
    minute = round(now.minute/10.)
        
    lastHour = hour
    lastMinute = minute
    return True

# Print the usage
usage()

# Get all of the useful values
g = guppi_status()
g.read()
nChan = g["OBSNCHAN"]
npoln = g["NPOL"]
BW = g["OBSBW"]
fctr = g["OBSFREQ"]
bins = n.arange(nChan)
freqs = (bins/float(nChan))*BW + (fctr-0.5*BW)
print 'NChan, Npol:',nChan,npoln
print 'freq,    bw:',fctr,BW

# Access the data buffer
d = guppi_databuf()
bdata = d.data(0) # argument is the block in the data buffer
adata = n.fromstring( bdata, n.int16)
data =  adata.byteswap()
data =  bdata
#d.dtype = n.int32
dataLen = len(data)
# Sum different amount depending on nChan
nspec_sum = blocksize / (2*nChan*npoln)
print "data dimensions:",data.ndim, dataLen,nspec_sum

if bdata.ndim == 1:
    print "data    X:", data.shape[0]
    print "N spectra:", data.shape[0]/nChan
    redata = n.reshape( data, (-1,nChan,1))
    if redata.ndim == 3:
        print "redata:", redata.shape[0],redata.shape[1],redata.shape[2]
    if view_mean:
        main_spec = redata[:nspec_sum,:,0].mean(0)
    else:
        main_spec = redata[:nspec_sum,:,0].std(0)
    print 'Main: ',main_spec[(nChan/2):((nChan/2)+3)]
    min_spec = redata[:nspec_sum,:,0].min(0)
    max_spec = redata[:nspec_sum,:,0].max(0)
if bdata.ndim == 3:
    print 'nChan,nPol,iPol,Shape: ',nChan,npoln,iPol, bdata.shape
# next step organizes the data into 4 blocks
    redata = n.reshape( data, (-1,nChan,npoln))
    print "data    X, Y, Z:", bdata.shape[0], bdata.shape[1], bdata.shape[2]
    print "redata  X, Y, Z:", redata.shape[0], redata.shape[1], redata.shape[2]
    nspec_sum = redata.shape[0]-1
    min_spec = redata[:nspec_sum,:,iPol].min(0)
    max_spec = redata[:nspec_sum,:,iPol].max(0)
    if view_mean:
        main_spec = redata[:nspec_sum,:,iPol].mean(0)
    else:
        main_spec = redata[:nspec_sum,:,iPol].std(0)
ymin = main_spec.min(0)
ymax = main_spec.max(0)

# Initialize the plot
fig = p.figure()
fig.canvas.mpl_connect('key_press_event', key_press)
ax = fig.add_subplot(111) # #vert, #horiz, winnum
ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Arbitrary Power')
#ax.set_title("Poln is '%s'"%polns[poln])
# save the clean slate background -- everything but the animated line
# is drawn and saved in the pixel buffer background
background = fig.canvas.copy_from_bbox(ax.bbox)
nX = main_spec.shape[0]
nF = freqs.shape[0]
bins = n.arange(nChan)
freqs = bins/float(nChan)*BW + (fctr-0.5*BW)
#print 'Main Spec: ',main_spec.shape
#If spectra not yet initialized set to frequency axis
if (plotCount < 3):
    main_spec = freqs
    max_spec = freqs
    min_spec = freqs
plotCount = plotCount + 1
main_line, = ax.plot(freqs, main_spec, 'r')
max_line, = ax.plot(freqs, max_spec, 'b:')
min_line, = ax.plot(freqs, min_spec, 'b:')
ax.axis([freqs.min(),freqs.max(),-1,2000])
fig.canvas.draw()

# Start the event loop
#gobject.idle_add(update_lines)
gobject.timeout_add(1000,update_lines)
try:
    p.show()
except KeyboardInterrupt:
    print "Exiting.."

