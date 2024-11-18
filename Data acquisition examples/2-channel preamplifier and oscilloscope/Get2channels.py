# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 18:09:04 2023

@author: XabierGC
"""

# Getting waveforms of channels 1 and 2 of TBS oscilloscope
# python v3.x, pyvisa v1.8
# should work with TDS2k, TPS2k, and TBS1k series

#%% Install before use
'''
Problems with NIvisa on Mac, preferably use PC

Must install these packages in anaconda prompt for code to run:

   conda install -c conda-forge pyvisa 
   conda install -c conda-forge pyvisa-py 
   conda install -c conda-forge pyusb 

Then install NI-VISA from:

https://www.ni.com/en-gb/support/downloads/drivers/download.ni-visa.html#442805
'''

import time # std module
import pyvisa as visa # http://github.com/hgrecco/pyvisa
import pylab as pl # http://matplotlib.org/
import numpy as np # http://www.numpy.org/

visa_address = 'USB0::0x0699::0x03C7::C020294::INSTR'

rm = visa.ResourceManager()
scope = rm.open_resource(visa_address)
scope.timeout = 10000 # ms
scope.encoding = 'latin_1'
scope.write_termination = None
scope.write('*cls') # clear ESR

print(scope.query('*idn?'))


#scope.write('*rst') # reset
#t1 = time.perf_counter()
r = scope.query('*opc?') # sync
#t2 = time.perf_counter()
#print('reset time: {} s'.format(t2 - t1))

#scope.write('autoset EXECUTE') # autoset
#t3 = time.perf_counter()
r = scope.query('*opc?') # sync
#t4 = time.perf_counter()
#print('autoset time: {} s'.format(t4 - t3))

# disable all channels but channel 1 and channel 2
scope.write('SELECT:CH1 1;CH2 1;CH3 0;CH4 0;MATH 0;REFA 0;REFB 0;REFC 0;REFD 0;')


# io config
scope.write('header 0')
scope.write('data:encdg RIBINARY')
scope.write('data:source CH1') # channel
scope.write('data:start 1') # first sample
record = int(scope.query('HOR:RECO?'))
scope.write('data:stop {}'.format(record)) # last sample
scope.write('wfmpre:byt_nr 1') # 1 byte per sample

# acq config
scope.write('acquire:state 0') # stop
scope.write('acquire:stopafter SEQUENCE') # single
scope.write('acquire:state 1') # run
#t5 = time.perf_counter()
r = scope.query('*opc?') # sync
#t6 = time.perf_counter()
#print('acquire time: {} s'.format(t6 - t5))

# data query
#t7 = time.perf_counter()
bin_wave1 = scope.query_binary_values('curve?', datatype='b', container=np.array)
#t8 = time.perf_counter()
#print('transfer time: {} s'.format(t8 - t7))

# retrieve scaling factors
tscale = float(scope.query('wfmpre:xincr?'))
tstart = float(scope.query('wfmpre:xzero?'))
vscale = float(scope.query('wfmpre:ymult?')) # volts / level
voff = float(scope.query('wfmpre:yzero?')) # reference voltage
vpos = float(scope.query('wfmpre:yoff?')) # reference position (level)


scope.write('data:source CH2') # channel
scope.write('data:start 1') # first sample
record = int(scope.query('wfmpre:nr_pt?'))
scope.write('data:stop {}'.format(record)) # last sample
scope.write('wfmpre:byt_nr 1') # 1 byte per sample

r = scope.query('*opc?')
bin_wave2 = scope.query_binary_values('curve?', datatype='b', container=np.array)

vscale2 = float(scope.query('wfmpre:ymult?')) # volts / level
voff2 = float(scope.query('wfmpre:yzero?')) # reference voltage
vpos2 = float(scope.query('wfmpre:yoff?')) # reference position (level)

# error checking
r = int(scope.query('*esr?'))
print('event status register: 0b{:08b}'.format(r))
r = scope.query('allev?').strip()
print('all event messages: {}'.format(r))

scope.close()
rm.close()

# create scaled vectors
# horizontal (time)
total_time = tscale * record
tstop = tstart + total_time
scaled_time = np.linspace(tstart, tstop, num=record, endpoint=False)
# vertical (voltage)
unscaled_wave1 = np.array(bin_wave1, dtype='double') # data type conversion
scaled_wave1 = (unscaled_wave1 - vpos) * vscale + voff

unscaled_wave2 = np.array(bin_wave2, dtype='double') # data type conversion
scaled_wave2 = (unscaled_wave2 - vpos2) * vscale2 + voff2



# plotting

# pl.plot(scaled_wave1)
# pl.plot(scaled_wave2)
# pl.title('Waveforms') # plot label
# pl.xlabel('time (seconds)') # x label
# pl.ylabel('voltage (volts)') # y label
# pl.show()
